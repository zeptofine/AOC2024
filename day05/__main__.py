from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PageRule:
    before: int
    after: int

    def is_true(self, pages: list[int]) -> bool:
        try:
            before_idx = pages.index(self.before)
            after_idx = pages.index(self.after)
        except ValueError:
            return True

        return before_idx < after_idx

    def fix(self, pages: list[int]) -> None:
        try:
            before_idx = pages.index(self.before)
            after_idx = pages.index(self.after)
        except ValueError:
            return
        if before_idx < after_idx:
            return
        pages[before_idx], pages[after_idx] = pages[after_idx], pages[before_idx]


type Pages = list[list[int]]


def get_input() -> tuple[list[PageRule], Pages]:
    pth = Path(__file__).parent / "input"
    with pth.open() as f:
        it = map(str.strip, iter(f))
        # get rules
        rules = []
        for line in it:
            if not line:
                break
            before, after = map(int, line.split("|"))
            rule = PageRule(before, after)
            rules.append(rule)

        # get pages
        pages = [list(map(int, line.split(","))) for line in it]

    return rules, pages


rules, page_sets = get_input()

print(f"{len(rules)} rules")
print(f"{len(page_sets)} total sets")
# index the page rules for faster reference
ruledict: dict[int, list[PageRule]] = defaultdict(list)
for rule in rules:
    ruledict[rule.before].append(rule)
    ruledict[rule.after].append(rule)


def apply_rules(
    pages: list[int],
    relevant_rules: set[PageRule] | None = None,
) -> tuple[bool, list[PageRule]]:
    relevant_rules = relevant_rules or {
        rule for page in pages for rule in ruledict[page] if page in ruledict
    }
    rule_evaluations = [(rule, rule.is_true(pages)) for rule in relevant_rules]
    all_true = all(valid for _, valid in rule_evaluations)
    if all_true:
        return all_true, []

    return all_true, [rule for rule, valid in rule_evaluations if not valid]


def attempt_fix(pages: list[int]) -> bool:
    relevant_rules = {
        rule for page in pages for rule in ruledict[page] if page in ruledict
    }
    while not (v_invalid := apply_rules(pages, relevant_rules))[0]:
        invalid_rules = v_invalid[1]
        for rule in invalid_rules:
            rule.fix(pages)

    return v_invalid[0]


middle_sum = 0
valid_sets = []
invalid_sets = []
for pages in page_sets:
    is_valid, invalid_rules = apply_rules(pages)
    if is_valid:
        middle_sum += pages[len(pages) // 2]
        valid_sets.append(pages)
    else:
        invalid_sets.append(pages)

print(f"{len(valid_sets)} valid sets")
print(f"SUM of MIDDLES: {middle_sum}")

if invalid_sets:
    print(f"{len(invalid_sets)} invalid sets")
    print("Trying to fix incorrectly ordered sets...")
    middle_sum = 0
    for invalid in invalid_sets:
        attempt_fix(invalid)
        middle_sum += invalid[len(invalid) // 2]

    print(f"SUM of FIXED MIDDLES: {middle_sum}")
