"""Build the academic homepage. Python standard library only."""
import json
from html import escape as e
from pathlib import Path

root = Path(__file__).resolve().parent
c = json.loads((root / 'content.json').read_text(encoding='utf-8'))

translations = json.loads((root / 'content.zh.json').read_text(encoding='utf-8'))


def build(locale):
    is_zh = locale == 'zh-CN'
    def tr(text):
        return translations.get(text, text) if is_zh else text

    filename = 'zh.html' if is_zh else 'index.html'
    primary_name = c['name_zh'] if is_zh else c['name']
    secondary_name = c['name'] if is_zh else c['name_zh']
    secondary_lang = 'en' if is_zh else 'zh-CN'
    stop = '。' if is_zh else '.'

    def link(label, href, cls=''):
        target = ' target="_blank" rel="noopener noreferrer"' if cls in ('paper-link', 'paper-title-link') or href.endswith('.pdf') else ''
        return f'<a class="{cls}" href="{e(href, quote=True)}"{target}>{e(tr(label))}</a>'

    interests = ''.join(f'<li><strong>{e(tr(title))}:</strong> {e(tr(text))}{stop}</li>' for title, text in c['interests'])
    news = ''
    for n in c['news']:
        label = f'<time datetime="{n["date"]}">{e(n["label"])}</time>' if n['date'] else f'<span class="news-label">{e(n["label"])}</span>'
        target = n.get("href", "#" + n.get("paper", "awards"))
        news += f'<li>{label}<span class="news-text"><span aria-hidden="true">🎉</span> <a href="{e(target, quote=True)}">{e(tr(n["text"]))}</a></span></li>'
    papers = ''
    for p in c['papers']:
        author_parts = []
        for author in p['authors'].split(', '):
            author_html = f'<strong class="author-self">{e(author)}</strong>' if author == c['name'] else e(author)
            if author in p.get('co_first_authors', []):
                author_html += f'<sup class="equal-mark" aria-label="{tr("Co-first author")}">*</sup>'
            author_parts.append(author_html)
        authors = ', '.join(author_parts)
        authorship_note = f'<p class="authorship-note">{tr("* Equal contribution.")}</p>' if p.get('co_first_authors') else ''
        links = ''.join(link(label, href, 'paper-link') for label, href in p['links'])
        tag_detail = f'<span class="venue-tag-detail">{e(p["tag_detail"])}</span>' if p.get('tag_detail') else ''
        papers += f'''<article class="paper" id="{p['id']}">
          <div class="paper-visual"><a href="{p['image']}" aria-label="View {p['id']} figure"><img src="{p['image']}" alt="{e(tr(p['image_alt']))}" loading="lazy" width="360" height="220"></a><span class="venue-tag">{e(tr(p['tag']))}{tag_detail}</span></div>
          <div class="paper-body"><h3>{link(p['title'], p.get('url', p['links'][0][1]), 'paper-title-link')}</h3><p class="authors">{authors}</p>{authorship_note}<p class="venue">{e(tr(p['venue']))}</p><p class="paper-description">{e(tr(p['description']))}</p>
          <div class="paper-actions">{links}<details class="citation"><summary>BibTeX</summary><pre>{e(p['bibtex'])}</pre></details><span class="paper-status">{e(p['status'])}</span></div></div>
        </article>'''
    award_groups = [
        ('national', 'International & National Prizes', {'National', 'International'}),
        ('regional', 'Regional, Provincial & University Prizes', {'Regional', 'Provincial', 'University'}),
    ]
    awards = ''
    for group_id, title, levels in award_groups:
        entries = [a for a in c['awards'] if a[4] != 'Recipient' and
                   (group_id == 'national' if any(contest in a[2] for contest in ('(ICPC)', '(CCPC)')) else a[3] in levels)]
        # Keep the owner's award-priority order from content.json.
        items = ''
        for year, award, event, level, role in entries:
            items += f'<li><span class="award-year">{e(tr(year))}: </span>{e(tr(event))} <span class="award-parenthesis">(</span><span class="award-prize">{e(tr(award))}</span><span class="award-parenthesis">, </span><span class="award-role">{e(tr(role))}</span><span class="award-parenthesis">)</span></li>'
        awards += f'<div class="award-group"><h3 id="awards-{group_id}">{e(tr(title))}</h3><div class="award-window award-window-{group_id}" tabindex="0" role="region" aria-labelledby="awards-{group_id}"><ul class="awards">{items}</ul></div><p class="scroll-hint">{e(tr("↕ Scrollable"))}</p></div>'
    scholarships = ''
    for year, award, event, level, role in c['awards']:
        if role == 'Recipient':
            suffix = f', {e(tr(event))}' if event else ''
            scholarships += f'<li><span class="scholarship-year">{e(tr(year))}</span>, <strong>{e(tr(award))}</strong>{suffix}{stop}</li>'
    awards += f'<div class="award-group scholarships"><h3>{e(tr("Scholarships"))}</h3><ul class="awards">{scholarships}</ul></div>'

    language_switch = '<nav class="language-switch" aria-label="Language / 语言">'
    for code, label, page in [('en', 'English', 'index.html'), ('zh-CN', '中文', 'zh.html')]:
        current = ' aria-current="page"' if code == locale else ''
        language_switch += f'<a class="language-option" href="{page}" lang="{code}" hreflang="{code}"{current}>{label}</a>'
    language_switch += '</nav>'
    html = f'''<!doctype html>
    <html lang="{locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>{e(primary_name)} | {e(tr(c['affiliation']))}</title><meta name="description" content="{e(tr(c['about']), quote=True)}"><meta name="color-scheme" content="light"><link rel="icon" href="assets/favicon.svg"><link rel="stylesheet" href="assets/minimal-light.css"><link rel="stylesheet" href="assets/site.css"><link rel="alternate" hreflang="en" href="index.html"><link rel="alternate" hreflang="zh-CN" href="zh.html"><script src="assets/language.js" defer></script></head>
    <body><a class="skip-link" href="#main">{e(tr("Skip to content"))}</a>{language_switch}<div class="wrapper">
    <header class="profile"><img class="portrait" src="assets/portrait.jpg" width="142" height="142" alt="{e(tr("Portrait of Hanrui Chen"), quote=True)}">
    <h1>{e(primary_name)}<span lang="{secondary_lang}">{e(secondary_name)}</span></h1><p class="role">{e(tr(c['role']))}</p><p class="affiliation">{link('Hangzhou Dianzi University', 'https://www.hdu.edu.cn/')}<br>{link('ITMO University', 'https://en.itmo.ru/')}</p><p class="department">{e(tr("Computer Science and Technology"))}</p><p class="email">{link(c['email'], 'mailto:'+c['email'])}</p>
    <div class="profile-links">{link('CV ↗', 'assets/hanrui-chen-cv.pdf')}{link('Codeforces ↗', 'https://codeforces.com/profile/Sellaris')}</div>
    <nav aria-label="{e(tr("On this page"), quote=True)}"><a href="#about">{e(tr("About"))}</a><a href="#news">{e(tr("News"))}</a><a href="#publications">{e(tr("Publications"))}</a><a href="#awards">{e(tr("Honors"))}</a></nav>
    <p class="profile-note">{e(tr("Hangzhou, China"))}</p></header>
    <main id="main"><section id="about"><h2>{e(tr("About Me"))}</h2><p>{e(tr(c['about']))}</p><p>{e(tr(c['about_extra']))}</p><p>{e(tr(c['competitive_programming']))}</p></section>
    <section id="interests"><h2>{e(tr("Research Interests"))}</h2><ul class="interests">{interests}</ul></section>
    <section id="news"><h2>{e(tr("News"))}</h2><ol class="news-list">{news}</ol></section>
    <section id="publications"><h2>{e(tr("Publications"))}</h2><p class="section-note">{e(tr("Selected papers"))}</p>{papers}</section>
    <section id="awards"><h2>{e(tr("Honors & Awards"))}</h2>{awards}</section>
    <div class="site-footer"><span>© 2026 {e(primary_name)}</span><span>{e(tr("Based on"))} {link('Minimal Light', 'https://github.com/yaoyao-liu/minimal-light')}</span><a href="#about">{e(tr("Back to top ↑"))}</a></div>
    </main></div></body></html>'''
    (root / 'dist' / filename).write_text(html, encoding='utf-8')

for locale in ('en', 'zh-CN'):
    build(locale)
print(f"Built English and Chinese pages: {len(c['papers'])} publications, {len(c['news'])} news items each.")
