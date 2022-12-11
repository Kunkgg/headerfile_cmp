import difflib
import filecmp
import logging
import pathlib
import json
from dataclasses import dataclass, field, asdict
from functools import cached_property, partial
from typing import Dict, List, Tuple

from common.utils import readlines
from headerfile.parser import ParsedHeaderFile, CppSyntaxType, SyntaxElement

logger = logging.getLogger(__name__)


@dataclass
class ComparedSyntaxElement:
    name: str
    from_content: List[str] = field(repr=False)
    to_content: List[str] = field(repr=False)
    from_desc: str
    to_desc: str
    differ: difflib.HtmlDiff
    is_same: bool = field(init=False)
    diff_html: str = field(init=False, repr=False)

    def __post_init__(self):
        self.is_same = self.from_content == self.to_content
        self.diff_html = self.differ.make_table(
            self.from_content, self.to_content, self.from_desc, self.to_desc
        )


@dataclass
class ComparedSyntaxElementCollection:
    syntax_type: CppSyntaxType
    from_onlys: List[SyntaxElement] = field(default_factory=list)
    to_onlys: List[SyntaxElement] = field(default_factory=list)
    intersection: List[ComparedSyntaxElement] = field(default_factory=list)
    is_same: bool = field(init=False)
    diff_count: int = field(init=False)
    intersection_diffs: List[ComparedSyntaxElement] = field(init=False)

    def __post_init__(self):
        self.intersection_diffs = [
            common_compared
            for common_compared in self.intersection
            if not common_compared.is_same
        ]
        self.diff_count = (
            len(self.from_onlys) + len(self.to_onlys) + len(self.intersection_diffs)
        )
        self.is_same = self.diff_count == 0


@dataclass
class ComparedHeaderFile:
    from_fn: str
    to_fn: str
    from_desc: str
    to_desc: str
    is_text_same: bool
    is_interface_same: bool
    diff_count: int
    cmp_text: ComparedSyntaxElement
    cmp_includes: ComparedSyntaxElementCollection
    cmp_defines: ComparedSyntaxElementCollection
    cmp_enums: ComparedSyntaxElementCollection
    cmp_variables: ComparedSyntaxElementCollection
    cmp_structs: ComparedSyntaxElementCollection

    def __repr__(self):
        from_name = pathlib.Path(self.from_fn).name
        to_name = pathlib.Path(self.to_fn).name
        from_desc = self.from_desc
        to_desc = self.to_desc
        text_same = self.is_text_same
        interface_smae = self.is_interface_same
        diff_count = self.diff_count

        cmp_includes = self.cmp_includes.is_same
        cmp_defines = self.cmp_defines.is_same
        cmp_enums = self.cmp_enums.is_same
        cmp_variables = self.cmp_variables.is_same
        cmp_structs = self.cmp_structs.is_same

        return (
            f"<ComparedHeaderFile: [file from: {from_name}, to: {to_name}]"
            + f" [desc: from: {from_desc}, to: {to_desc}]"
            + f" [text_same: {text_same}] [interface_same: {interface_smae}]"
            + f" [diff_count: {diff_count}] [cmp_includes: {cmp_includes}]"
            + f" [cmp_defines: {cmp_defines}] [cmp_enums: {cmp_enums}]"
            + f" [cmp_variables: {cmp_variables}] [cmp_structs: {cmp_structs}]>"
        )

    def to_dict(self):
        return asdict(self)

    def to_json(self, fn, encoding="utf-8"):
        class ComparedHeaderFileJSONEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, difflib.HtmlDiff):
                    return "<difflib.HtmlDiff>"
                elif isinstance(obj, CppSyntaxType):
                    return obj.value
                return json.JSONEncoder.default(self, obj)

        with open(fn, "w", encoding=encoding) as fp:
            json.dump(self.to_dict(), fp, indent=2, cls=ComparedHeaderFileJSONEncoder)
        logger.info(f"Dumped ComparedHeaderFile to: {fn}")


class HeaderFileComparator:
    def __init__(
        self,
        from_: ParsedHeaderFile,
        to_: ParsedHeaderFile,
        from_desc: str = "from",
        to_desc: str = "to",
        differ=difflib.HtmlDiff(),
    ):
        self.from_ = from_
        self.to_ = to_
        self.from_desc = from_desc
        self.to_desc = to_desc
        self.differ = differ
        self.from_fn = pathlib.Path(self.from_.file).name
        self.to_fn = pathlib.Path(self.to_.file).name

    def compare(self):
        return ComparedHeaderFile(
            from_fn=str(self.from_fn),
            to_fn=str(self.to_fn),
            from_desc=self.from_desc,
            to_desc=self.to_desc,
            is_text_same=self.is_text_same,
            is_interface_same=self.is_interface_same,
            diff_count=self.diff_count,
            cmp_text=self.cmp_text,
            cmp_includes=self.cmp_includes,
            cmp_defines=self.cmp_defines,
            cmp_enums=self.cmp_enums,
            cmp_variables=self.cmp_variables,
            cmp_structs=self.cmp_structs,
        )

    @cached_property
    def is_text_same(self) -> bool:
        return filecmp.cmp(self.from_.file, self.to_.file)

    @cached_property
    def is_interface_same(self) -> bool:
        if self.is_text_same:
            return True

        cmps = []
        for syntax_type in CppSyntaxType:
            attr_name = f"cmp_{syntax_type.value}s"
            cmps.append(getattr(self, attr_name).is_same)
        return all(cmps)

    @cached_property
    def diff_count(self) -> int:
        if self.is_text_same:
            return 0

        cmps = []
        for syntax_type in CppSyntaxType:
            attr_name = f"cmp_{syntax_type.value}s"
            cmps.append(getattr(self, attr_name).diff_count)
        return sum(cmps)

    def to_dict(self) -> Dict:
        return self.compare().to_dict()

    def to_json(self, fn: str, encoding: str = "utf-8"):
        return self.compare().to_json(fn, encoding)

    @cached_property
    def from_lines(self):
        return readlines(self.from_.file)

    @cached_property
    def to_lines(self):
        return readlines(self.to_.file)

    def make_from_desc(self, desc_parts: List[str]) -> str:
        return "/".join([self.from_desc] + desc_parts)

    def make_to_desc(self, desc_parts: List[str]) -> str:
        return "/".join([self.to_desc] + desc_parts)

    @cached_property
    def cmp_text(self):
        from_desc = self.make_from_desc([self.from_fn])
        to_desc = self.make_to_desc([self.to_fn])
        return ComparedSyntaxElement(
            name="__text__",
            from_content=self.from_lines,
            to_content=self.to_lines,
            from_desc=from_desc,
            to_desc=to_desc,
            differ=self.differ,
        )

    def cmp_syntax_element_collection(self, syntax_type: CppSyntaxType):
        attr_name = f"{syntax_type.value}s"
        from_attr = getattr(self.from_, attr_name)
        to_attr = getattr(self.to_, attr_name)
        from_onlys = from_attr - to_attr
        to_onlys = to_attr - from_attr
        intersection_compares = self.cmp_syntax_element_collection_intersection(
            syntax_type
        )

        # from_onlys: List = field(default_factory=list)
        # to_onlys: List = field(default_factory=list)
        # intersection: List[ComparedSyntaxElement] = field(default_factory=list)
        return ComparedSyntaxElementCollection(
            syntax_type=syntax_type,
            from_onlys=from_onlys,
            to_onlys=to_onlys,
            intersection=intersection_compares,
        )

    def cmp_syntax_element_collection_intersection(
        self, syntax_type: CppSyntaxType
    ) -> List[ComparedSyntaxElement]:
        attr_name = f"{syntax_type.value}s"
        from_attr = getattr(self.from_, attr_name)
        to_attr = getattr(self.to_, attr_name)

        from_desc = self.make_from_desc([self.from_fn, attr_name])
        to_desc = self.make_to_desc([self.to_fn, attr_name])

        DescComparedSyntaxElement = partial(
            ComparedSyntaxElement,
            from_desc=from_desc,
            to_desc=to_desc,
            differ=self.differ,
        )

        intersection = from_attr.intersection(to_attr)
        extracted_intersection = [
            {
                "name": intersection_el.get("name"),
                "from_content": intersection_el.get("content"),
                "to_content": intersection_el.get("other_content"),
            }
            for intersection_el in intersection
        ]
        intersection_compares = [
            DescComparedSyntaxElement(**common_dict)
            for common_dict in extracted_intersection
        ]

        return intersection_compares

    @cached_property
    def cmp_includes(self) -> ComparedSyntaxElementCollection:
        return self.cmp_syntax_element_collection(CppSyntaxType.INCLUDE)

    @cached_property
    def cmp_includes_intersection(self):
        return self.cmp_syntax_element_collection_intersection(CppSyntaxType.INCLUDE)

    @cached_property
    def cmp_defines(self) -> ComparedSyntaxElementCollection:
        return self.cmp_syntax_element_collection(CppSyntaxType.DEFINE)

    @cached_property
    def cmp_defines_intersection(self):
        return self.cmp_syntax_element_collection_intersection(CppSyntaxType.DEFINE)

    @cached_property
    def cmp_enums(self) -> ComparedSyntaxElementCollection:
        return self.cmp_syntax_element_collection(CppSyntaxType.ENUM)

    @cached_property
    def cmp_enums_intersection(self):
        return self.cmp_syntax_element_collection_intersection(CppSyntaxType.ENUM)

    @cached_property
    def cmp_variables(self) -> ComparedSyntaxElementCollection:
        return self.cmp_syntax_element_collection(CppSyntaxType.VARIABLE)

    @cached_property
    def cmp_variables_intersection(self):
        return self.cmp_syntax_element_collection_intersection(CppSyntaxType.VARIABLE)

    @cached_property
    def cmp_structs(self) -> ComparedSyntaxElementCollection:
        return self.cmp_syntax_element_collection(CppSyntaxType.STRUCT)

    @cached_property
    def cmp_structs_intersection(self):
        return self.cmp_syntax_element_collection_intersection(CppSyntaxType.STRUCT)

