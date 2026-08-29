#!/usr/bin/env python3
"""Flag common over-polished AI-style surface patterns in Chinese drafts."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SCAFFOLD_MARKERS = (
    "先把边界说清楚",
    "这三条线必须分开",
    "最后还有一层",
    "真正值得讨论的地方",
    "这件事反映出的，不只是",
)
NARRATIVE_DECONSTRUCTION_PATTERNS = (
    r"(?:但|可).{0,12}(?:看完|仔细看).{0,24}(?:发现|会发现).{0,20}(?:没有那么|没那么)",
    r"事情其实没有那么(?:痛快|简单)",
    r"准确地说，.{0,30}(?:只是|小插曲|并不是)",
)
PROP_REFRAMING_PATTERNS = (
    r"这(?:句话|个细节|副[^，。\n]{0,8}).{0,16}比[^，。\n]{1,16}重要得多",
    r"最荒诞的不是[^。]{1,50}。?\s*是[^。]{1,80}(?:显得|变得).{0,12}(?:合理|正常)",
)
REDEFINITION_PATTERNS = (
    r"说得直白一点，.{0,40}(?:已经不是|更像)",
    r"这(?:已经|就)不是[^。]{1,40}。?\s*它更像",
)
SCIENCE_BALANCE_PATTERNS = (
    r"(?:是|算)件?好事.{0,120}(?:但是|但|不过).{0,120}(?:也|不能|麻烦|坏处)",
    r"(?:有帮助|有好处).{0,100}(?:但|不过|麻烦).{0,100}(?:损失|刨|啄|坏处)",
    r"这件事不用非得选一边",
)
WARM_SCIENCE_ENDING_PATTERNS = (
    r"春天.{0,30}田埂.{0,100}(?:生命|生机|位置)",
    r"(?:给|为).{0,30}(?:生命|动物).{0,20}(?:留|留下).{0,12}(?:位置|空间)",
    r"人与自然.{0,30}(?:关系|相处|和谐)",
)
CONTENT_INFO_DUMP_PATTERNS = (
    r"(?:公开资料显示|相关信息显示|已有信息显示|资料显示|据报道).{0,160}(?:总的来说|综上|因此).{0,80}(?:具有|有).{0,20}(?:参考|借鉴|启发|意义|帮助)",
    r"(?:复用他人观点|搬运客观信息|主题明确|表达清晰|论据充分|干货价值).{0,120}(?:用户|读者).{0,20}(?:获得感|提供参考|产生帮助)",
)
GENERIC_VALUE_ADVICE_PATTERNS = (
    r"(?:提高|提升)(?:个人)?认知.{0,80}(?:加强|持续|保持).{0,80}(?:沟通|积累|学习|理性|输出)",
    r"(?:持续输出|多输出).{0,20}(?:有价值|高质量).{0,30}(?:内容|观点)",
    r"(?:保持理性|理性看待).{0,60}(?:加强|提高|提升).{0,60}(?:沟通|认知|学习)",
)
SHOWY_POLISH_TERMS = (
    "一种奢侈",
    "更是稀有",
    "火上浇油",
    "璀璨",
    "深厚底蕴",
    "得天独厚",
    "赋能",
    "致力于",
    "重塑",
    "重新定义",
)
OVER_PACKAGED_SIMPLE_PATTERNS = (
    r"给自己定(?:一个)?[^。！？\n]{0,20}版本",
    r"简历也别写成自我介绍",
    r"(?:目标|计划|步骤|安排)[^。！？\n]{0,20}(?:版本|框架|系统)",
)
UNATTRIBUTED_SPECIFICITY_PATTERNS = (
    r"(?:一天下来|一天里|一整天)[^。！？\n]{0,50}(?:几十|几百|上百|无数)次",
    r"(?:短短|不到)[^，。！？\n]{0,12}(?:一天|一周|一个月)[^。！？\n]{0,50}(?:几十|几百|上百|无数)次",
)
AI_COLD_ASIDE_PATTERNS = (
    r"这(?:句)?话(?:可能)?有点冷",
    r"这(?:句)?话(?:很|有点|可能有点)?冷[，,。；;]?(?:但|不过).{0,16}(?:真实|实用|管用|有用)",
    r"这(?:句)?话说得(?:难听|冷).{0,16}(?:但|不过).{0,16}(?:真实|实用|管用|有用)",
)
LABEL_THEN_CONTRAST_PATTERNS = (
    r"这(?:句)?话[^。！？\n]{0,16}(?:很|有点|可能有点)(?:冷|真实|现实|难听|残酷|实用|管用|重要)"
    r"[^。！？\n]{0,20}(?:但|不过|却|会|能)",
    r"这个(?:判断|说法|问题|地方|逻辑|结论|建议|动作|选择|方法|现实)"
    r"[^。！？\n]{0,16}(?:很|有点|可能有点)(?:冷|真实|现实|难听|残酷|实用|管用|重要)"
    r"[^。！？\n]{0,20}(?:但|不过|却|会|能)",
)
EVALUATIVE_NOT_BUT_OPENING_PATTERNS = (
    r"(?:最(?:刺眼|扎心|危险|荒诞|讽刺|要命|麻烦|离谱|让人(?:窒息|难受))|真正(?:可怕|麻烦|危险|要命))"
    r"[^。！？\n]{0,30}(?:不是|并非)[^。！？\n]{1,80}(?:而是|，是)",
)
VAGUE_IMAGE_PLACEMENT_PATTERNS = (
    r"(?:插入位置|放置位置|配图位置)[：:\s]*(?:开头|中间|中段|后面|结尾|正文中|责任部分附近)",
    r"(?:图一|图二|图三)[：:][^。！？\n]{0,40}(?:插在|放在)(?:开头|中间|中段|后面|结尾|正文中)",
)
NOT_BUT_PATTERN = r"(?:不是|并非)[^。！？；\n]{1,60}(?:而是|，是)"
CONTRAST_REFRAME_PATTERNS = (
    NOT_BUT_PATTERN,
    r"不在于[^。！？；\n]{1,60}而在于",
    r"不只是[^。！？；\n]{1,60}(?:更是|还在于|也在于)",
)


def _paragraphs(text: str) -> list[str]:
    return [
        re.sub(r"\s+", " ", paragraph).strip()
        for paragraph in re.split(r"\n\s*\n", text)
        if paragraph.strip()
    ]


def _count_pattern_hits(text: str, patterns: tuple[str, ...]) -> int:
    return sum(len(re.findall(pattern, text)) for pattern in patterns)


def analyze_text(text: str) -> list[str]:
    """Return stable issue identifiers for high-risk style patterns."""
    issues: set[str] = set()
    paragraphs = _paragraphs(text)
    if any(marker in text for marker in SCAFFOLD_MARKERS):
        issues.add("explicit-scaffold")
    if text.count("不等于") >= 3:
        issues.add("symmetric-negation-run")
    if len(re.findall(r"谁来[^？?\n]{0,40}[？?]", text)) >= 3:
        issues.add("rhetorical-question-barrage")
    if len(re.findall(r"把[^，。\n]{1,30}(?:压缩|包装)成", text)) >= 2:
        issues.add("analytic-parallelism")
    not_but_hits = len(re.findall(NOT_BUT_PATTERN, text))
    if not_but_hits >= 1:
        issues.add("not-but-template")
    if not_but_hits >= 2:
        issues.add("not-but-overuse")
    if any(len(re.findall(NOT_BUT_PATTERN, paragraph)) >= 2 for paragraph in paragraphs):
        issues.add("not-but-cluster")
    contrast_hits_by_paragraph = [
        _count_pattern_hits(paragraph, CONTRAST_REFRAME_PATTERNS) for paragraph in paragraphs
    ]
    if sum(contrast_hits_by_paragraph) >= 3:
        issues.add("contrast-reframe-overuse")
    if any(hits >= 2 for hits in contrast_hits_by_paragraph):
        issues.add("contrast-reframe-cluster")
    if any(
        left_hits and right_hits
        for left_hits, right_hits in zip(
            contrast_hits_by_paragraph, contrast_hits_by_paragraph[1:]
        )
    ):
        issues.add("contrast-reframe-adjacent-paragraphs")
    if any(re.search(pattern, text, re.DOTALL) for pattern in NARRATIVE_DECONSTRUCTION_PATTERNS):
        issues.add("viral-story-deconstruction")
    if any(re.search(pattern, text, re.DOTALL) for pattern in PROP_REFRAMING_PATTERNS):
        issues.add("prop-reframing")
    if any(re.search(pattern, text, re.DOTALL) for pattern in REDEFINITION_PATTERNS):
        issues.add("problem-redefinition-template")
    science_balance_hits = sum(
        bool(re.search(pattern, text, re.DOTALL)) for pattern in SCIENCE_BALANCE_PATTERNS
    )
    if science_balance_hits >= 2:
        issues.add("balanced-science-template")
    if any(re.search(pattern, text, re.DOTALL) for pattern in WARM_SCIENCE_ENDING_PATTERNS):
        issues.add("warm-science-ending")
    if any(re.search(pattern, text, re.DOTALL) for pattern in CONTENT_INFO_DUMP_PATTERNS):
        issues.add("source-copy-without-take")
    if any(re.search(pattern, text, re.DOTALL) for pattern in GENERIC_VALUE_ADVICE_PATTERNS):
        issues.add("generic-value-advice")
    showy_polish_hits = sum(text.count(term) for term in SHOWY_POLISH_TERMS)
    if showy_polish_hits >= 2:
        issues.add("showy-polish-cluster")
    if any(re.search(pattern, text, re.DOTALL) for pattern in OVER_PACKAGED_SIMPLE_PATTERNS):
        issues.add("over-packaged-simple-wording")
    if any(re.search(pattern, text, re.DOTALL) for pattern in UNATTRIBUTED_SPECIFICITY_PATTERNS):
        issues.add("unattributed-specificity")
    if any(re.search(pattern, text, re.DOTALL) for pattern in AI_COLD_ASIDE_PATTERNS):
        issues.add("cold-aside-template")
    if any(re.search(pattern, text, re.DOTALL) for pattern in LABEL_THEN_CONTRAST_PATTERNS):
        issues.add("label-then-contrast-template")
    first_paragraph = paragraphs[0] if paragraphs else ""
    if any(
        re.search(pattern, first_paragraph, re.DOTALL)
        for pattern in EVALUATIVE_NOT_BUT_OPENING_PATTERNS
    ):
        issues.add("evaluative-not-but-opening")
    if any(re.search(pattern, text, re.DOTALL) for pattern in VAGUE_IMAGE_PLACEMENT_PATTERNS):
        issues.add("vague-image-placement")
    conclusion_stack_hits = len(
        re.findall(r"(?:本质上|核心在于|说明了|反映出|值得反思|具有重要意义)", text)
    )
    if conclusion_stack_hits >= 4:
        issues.add("unsupported-conclusion-stack")

    short_run = 0
    for paragraph in paragraphs:
        if len(paragraph) >= 360 and len(re.findall(r"[。！？；]", paragraph)) >= 6:
            issues.add("wall-of-text")
        is_short = len(paragraph) <= 34 and not paragraph.startswith(("#", "-", "*", ">"))
        short_run = short_run + 1 if is_short else 0
        if short_run >= 3:
            issues.add("short-paragraph-run")
            break
    return sorted(issues)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", help="UTF-8 Markdown or text draft to inspect")
    args = parser.parse_args()
    text = Path(args.draft).read_text(encoding="utf-8")
    issues = analyze_text(text)
    if not issues:
        print("[OK] no configured over-polished style patterns found")
        return 0
    for issue in issues:
        print(f"[WARN] {issue}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
