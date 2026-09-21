import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# The clean, perfectly structured HTML for the 3 team member cards
clean_team_items = '''<div class="team-members-main-collection-item w-dyn-item" role="listitem">
<div class="team-member-wrapper sai-3d-fan-left">
<div class="team-member-image-wrapper">
<img alt="Luthfi Muthatohirin" class="team-member-image" loading="lazy" src="assets/ritovex/Luthfi.png"/>
<div class="team-member-social-media-wrapper">
<a class="team-member-social-media-link-block w-inline-block" href="https://www.instagram.com/saitech_id/" rel="noopener noreferrer" target="_blank" title="Instagram: @saitech_id">\uf16d</a>
<a class="team-member-social-media-link-block w-inline-block" href="https://www.tiktok.com/@saitech.officialid" rel="noopener noreferrer" target="_blank" title="TikTok: @saitech.officialid">\ue07b</a>
</div>
</div>
<div class="team-member-typography">
<a class="team-member-name" href="#">Luthfi Muthatohirin</a>
<div class="team-member-bio">AI Engineer Lead &amp; Data Engineer</div>
</div>
</div>
</div>
<div class="team-members-main-collection-item w-dyn-item" role="listitem">
<div class="team-member-wrapper sai-3d-fan-center">
<div class="team-member-image-wrapper">
<img alt="Erlin Sari" class="team-member-image" loading="lazy" src="assets/ritovex/Erlin.png"/>
<div class="team-member-social-media-wrapper">
<a class="team-member-social-media-link-block w-inline-block" href="https://www.instagram.com/saitech_id/" rel="noopener noreferrer" target="_blank" title="Instagram: @saitech_id">\uf16d</a>
<a class="team-member-social-media-link-block w-inline-block" href="https://www.tiktok.com/@saitech.officialid" rel="noopener noreferrer" target="_blank" title="TikTok: @saitech.officialid">\ue07b</a>
</div>
</div>
<div class="team-member-typography">
<a class="team-member-name" href="#">Erlin Sari</a>
<div class="team-member-bio">UI-UX Designer &amp; Data Engineer</div>
</div>
</div>
</div>
<div class="team-members-main-collection-item w-dyn-item" role="listitem">
<div class="team-member-wrapper sai-3d-fan-right">
<div class="team-member-image-wrapper">
<img alt="Sabilillah Irdo" class="team-member-image" loading="lazy" src="assets/ritovex/Sabil.png"/>
<div class="team-member-social-media-wrapper">
<a class="team-member-social-media-link-block w-inline-block" href="https://www.instagram.com/saitech_id/" rel="noopener noreferrer" target="_blank" title="Instagram: @saitech_id">\uf16d</a>
<a class="team-member-social-media-link-block w-inline-block" href="https://www.tiktok.com/@saitech.officialid" rel="noopener noreferrer" target="_blank" title="TikTok: @saitech.officialid">\ue07b</a>
</div>
</div>
<div class="team-member-typography">
<a class="team-member-name" href="#">Sabilillah Irdo</a>
<div class="team-member-bio">Scrum Master &amp; Full-Stack Developer</div>
</div>
</div>
</div>'''

def fix_file(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the team section
    # Match from <div class="team-members-main-collection-list w-dyn-items" role="list"> to </section>
    pattern = r'(<div class="team-members-main-collection-list w-dyn-items" role="list">)[\s\S]*?(</section>)'
    
    replacement = r'\1\n' + clean_team_items + '\n</div>\n</div>\n</div>\n</div>\n\\2'
    
    new_content, count = re.subn(pattern, replacement, content)
    if count > 0:
        # Also fix any stray trailing </div> right after </section>
        new_content = new_content.replace('</section></div>\n\n\n\n<!-- Section Standar', '</section>\n\n\n\n<!-- Section Standar')
        new_content = new_content.replace('</section></div>\n\n\n\n<section class="section cta">', '</section>\n\n\n\n<section class="section cta">')
        new_content = new_content.replace('</section></div>\n\n\n<section class="section cta">', '</section>\n\n\n<section class="section cta">')

        with open(fname, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"SUCCESS: Fixed team cards structure in {fname}")
    else:
        print(f"FAILED to match pattern in {fname}")

fix_file('about.html')
fix_file('team.html')
