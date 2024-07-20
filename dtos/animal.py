from dataclasses import dataclass


@dataclass
class Animal:
    name: str
    name_for_url: str
    image_src: str
    collateral_adjectives: list[str]

    def __init__(self, name, name_for_url, image_src, collateral_adjectives):
        self.name = self._fix_string_from_html(name)
        self.name_for_url = name_for_url
        self.image_src = image_src
        self.collateral_adjectives = self._fix_collateral_adjectives(collateral_adjectives)

    @classmethod
    def _fix_string_from_html(cls, string_from_html: str) -> str:
        if '/' in string_from_html:
            fixed_string_from_html = string_from_html.split('/')[0]
        else:
            fixed_string_from_html = string_from_html
        return fixed_string_from_html

    @classmethod
    def _fix_collateral_adjectives(cls, collateral_adjectives):
        fixed_collateral_adjectives = []
        for collateral_adjective in collateral_adjectives:
            if collateral_adjective == '—':
                fixed_collateral_adjectives.append('No Collateral Adjectives')
            else:
                fixed_collateral_adjectives.append(collateral_adjective)
        return fixed_collateral_adjectives
