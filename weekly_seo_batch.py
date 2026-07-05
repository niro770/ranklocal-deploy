#!/usr/bin/env python3
"""
weekly_seo_batch.py
-------------------
Automated weekly SEO batch for ranklocall.com
- Reads topic_queue.json, picks next 50 pending topics
- Generates humanized HTML pages with schema + internal links
- Updates sitemap.xml and google-indexing.yml
- Commits and pushes to GitHub
- Pings Google sitemap

Run: python weekly_seo_batch.py
Schedule: every Sunday (Cowork scheduled task)
"""

import json, os, hashlib, subprocess, datetime, urllib.request, urllib.error, sys

# ── CONFIG ──────────────────────────────────────────────────────────────────
BASE        = r"C:\Users\19522\Documents\ranklocal-deploy-push"
QUEUE_PATH  = os.path.join(BASE, "topic_queue.json")
SITEMAP     = os.path.join(BASE, "sitemap.xml")
YML_PATH    = os.path.join(BASE, ".github", "workflows", "google-indexing.yml")
LOG_PATH    = os.path.join(BASE, "weekly_seo_batch.log")
BATCH_SIZE  = 50
SITE        = "https://ranklocall.com"

_now       = datetime.datetime.now()
MONTH_YEAR = _now.strftime("%B %Y")
BYLINE     = ('By <a href="/about/">Nir Barlev</a>, Founder &amp; CEO'
              ' &middot; Updated ' + MONTH_YEAR)

PERSON_SCHEMA = {
    "@type": "Person", "@id": "https://ranklocall.com/#founder",
    "name": "Nir Barlev", "jobTitle": "Founder & CEO",
    "url": "https://ranklocall.com/about/",
    "sameAs": ["https://www.linkedin.com/in/nir-barlev/"]
}

NAV = ('<nav class="site-nav">'
       '<a href="/">Home</a>'
       '<a href="/contractor-leads/">Contractor Leads</a>'
       '<a href="/pay-per-call/">Pay-Per-Call</a>'
       '<a href="/appointment-setting/">Appointment Setting</a>'
       '<a href="/about/">About</a>'
       '<a href="/apply/" class="cta-btn">Get Leads</a>'
       '</nav>')

FOOTER = ('<footer class="site-footer">'
          '<p>&copy; 2025 RankLocal &bull; '
          '<a href="/privacy/">Privacy</a> &bull; '
          '<a href="/terms/">Terms</a></p>'
          '</footer>')

# ── TRADE DATA ───────────────────────────────────────────────────────────────
# Each entry: bodies = list of paragraph variants (picked by slug hash)
# faq_templates = list of (question, answer) pairs
# related_links = [(href, text), ...]

TRADE_DATA = {
    "Roofing": {
        "lead_page": "/roofing-leads/",
        "marketing_page": "/roofing-marketing-guide/",
        "avg_job": "$8,000-18,000",
        "cpl": "$75-130",
        "close_rate": "25-35%",
        "services": "roof replacement, leak repair, storm damage assessment, and shingle repair",
        "bodies": [
            ("Roofing contractors operate project-to-project, and the gap between jobs is where revenue gets lost. The contractors who stay consistently booked invest in exclusive inbound lead sources rather than competing for shared marketplace contacts. When a homeowner calls you after searching specifically for a roofer in their area, that conversation starts from a position of intent -- they have a need, they found you, and they called. Close rates on exclusive inbound roofing calls run 25-35%, compared to 8-12% for shared form leads from Angi or HomeAdvisor.",
             "Storm damage, aging shingles, and active leaks are the three primary triggers for roofing calls -- and each one represents a homeowner who has decided they need professional help. That decision-point is exactly where exclusive inbound calls capture demand. Rather than paying for a shared lead that goes to four other roofers simultaneously, you receive a single inbound call from a homeowner who searched, found your number, and called. No competing contractors. No race-to-call dynamic. Just a qualified homeowner who needs a roofer."),
        ],
        "faqs": [
            ("How do exclusive roofing leads work?",
             "An exclusive roofing lead is an inbound phone call delivered only to your business. The homeowner searched for roofing services, found your number, and called. You pay per qualified call over 60 seconds in your service area -- no competing contractors receive the same contact."),
            ("What roofing services generate the most inbound calls?",
             "Storm damage assessment, full roof replacement, shingle repair, leak repair, and emergency tarping generate the highest roofing call volumes. Storm events create significant demand spikes."),
            ("What is the close rate on exclusive roofing calls?",
             "Exclusive inbound roofing calls close at 25-35% on average -- versus 8-12% for shared form-fill leads. Emergency calls (active leak, visible storm damage) close at 40%+ when same-day response is available."),
        ],
        "links": [("/roofing-leads/", "Roofing Lead Generation"),
                  ("/roofing-marketing-guide/", "Roofing Marketing Guide"),
                  ("/pay-per-call/", "Pay-Per-Call Lead Generation"),
                  ("/exclusive-vs-shared-leads/", "Exclusive vs Shared Leads")],
    },
    "HVAC": {
        "lead_page": "/hvac-leads/",
        "marketing_page": "/hvac-marketing-guide/",
        "avg_job": "$2,500-8,000",
        "cpl": "$45-90",
        "close_rate": "28-40%",
        "services": "AC repair, heating repair, system replacement, and heat pump installation",
        "bodies": [
            ("HVAC is one of the few home services categories with true same-day emergency demand. When an AC fails in the middle of summer or a furnace stops in January, the homeowner needs a technician today -- not next week, not after getting three estimates. That urgency produces some of the highest inbound call intent in home services. An exclusive HVAC call from a homeowner whose system failed closes at 45-55% when you can confirm same-day availability on the call.",
             "Seasonal demand peaks create significant revenue windows for HVAC contractors -- and missing those peaks because of insufficient lead volume is the most common growth limiter in the industry. Referrals and organic traffic alone rarely keep up with peak-week call volume. A pay-per-call lead channel fills that gap: you get exclusive calls while demand is running high, at a cost that aligns with the high job values those calls produce."),
        ],
        "faqs": [
            ("How do exclusive HVAC leads work?",
             "Exclusive HVAC leads are inbound phone calls from homeowners with active heating or cooling needs, delivered only to your business. You pay per qualified call over 60 seconds in your service area."),
            ("What HVAC services generate the most calls?",
             "Emergency AC repair and furnace failure generate the highest call urgency. System replacement, heat pump installation, and annual tune-up calls provide consistent baseline volume year-round."),
            ("What is the close rate on exclusive HVAC calls?",
             "Exclusive HVAC calls close at 28-40% overall. Emergency failure calls close at 45-55% when same-day service is offered and confirmed on the initial call."),
        ],
        "links": [("/hvac-leads/", "HVAC Lead Generation"),
                  ("/hvac-marketing-guide/", "HVAC Marketing Guide"),
                  ("/pay-per-call/", "Pay-Per-Call Lead Generation"),
                  ("/exclusive-vs-shared-leads/", "Exclusive vs Shared Leads")],
    },
    "Plumbing": {
        "lead_page": "/plumbing-leads/",
        "marketing_page": "/plumbing-marketing-guide/",
        "avg_job": "$500-4,000",
        "cpl": "$40-75",
        "close_rate": "28-38%",
        "services": "emergency plumbing, drain cleaning, water heater replacement, and pipe repair",
        "bodies": [
            ("Plumbing has a consistent mix of emergency demand (burst pipes, major drain clogs, water heater failures) and project-based demand (remodels, fixture upgrades, water line replacements) that produces reliable call volume year-round. Emergency calls close at 50%+ when answered and responded to quickly. Project calls take slightly longer but carry higher average values. The combination makes plumbing one of the best performing trades for exclusive inbound call ROI.",
             "The primary competitive advantage in plumbing isn't price -- it's availability and responsiveness. A homeowner with a burst pipe will hire the first licensed plumber who answers the phone and says they can be there within two hours. Exclusive inbound calls put you in that position: you receive the call, assess the urgency, and confirm your availability. No other plumber received the same call. The job is yours if you can show up."),
        ],
        "faqs": [
            ("How do exclusive plumbing leads work?",
             "Exclusive plumbing leads are inbound phone calls from homeowners in your service area who searched for a plumber and called. You pay per qualified call over 60 seconds. No competing plumbers receive the same contact."),
            ("What plumbing services generate the most calls?",
             "Emergency calls (burst pipes, major drain clogs, water heater failures) generate the highest urgency and volume. Water line repair, slab leak detection, and remodel plumbing produce the highest average ticket values."),
            ("What is the close rate on exclusive plumbing calls?",
             "Exclusive inbound plumbing calls close at 28-38% overall. Emergency calls (active water event) close at 50%+ when same-day response is confirmed on the initial call."),
        ],
        "links": [("/plumbing-leads/", "Plumbing Lead Generation"),
                  ("/plumbing-marketing-guide/", "Plumbing Marketing Guide"),
                  ("/pay-per-call/", "Pay-Per-Call Lead Generation"),
                  ("/exclusive-vs-shared-leads/", "Exclusive vs Shared Leads")],
    },
    "Pest Control": {
        "lead_page": "/pest-control-leads/",
        "marketing_page": "/pest-control-marketing-guide/",
        "avg_job": "$150-1,500",
        "cpl": "$25-75",
        "close_rate": "30-45%",
        "services": "general pest control, termite treatment, rodent removal, and bed bug treatment",
        "bodies": [
            ("Pest control is a category where homeowners typically hire on the same call they made to ask about the service. By the time someone calls a pest control company, they've already confirmed there's a problem and decided they're not handling it themselves. That pre-qualification makes inbound pest calls among the highest-converting in home services. The key metric isn't close rate on individual calls -- it's lifetime value from recurring service agreements that convert from those first calls.",
             "Recurring service plans are where pest control businesses build predictable revenue. A one-time treatment is a $150-400 job. A quarterly plan is $600-1,200 per year from the same customer, every year. Contractors who convert inbound calls to annual agreements build a revenue base that compounds over time. The exclusive inbound call is the acquisition point; the recurring plan is where the real return on that call cost materializes."),
        ],
        "faqs": [
            ("How do exclusive pest control leads work?",
             "Exclusive pest control leads are inbound phone calls from homeowners with active pest issues, delivered only to your company. You pay per qualified call over 60 seconds in your service area."),
            ("What pests generate the most service calls?",
             "Termites, cockroaches, ants, rodents, bed bugs, and mosquitoes generate the highest call volumes. Termite calls carry the highest average ticket values in the pest control category."),
            ("What is the close rate on exclusive pest calls?",
             "Exclusive inbound pest calls close at 30-45% for initial service. Converting those customers to recurring quarterly plans runs 60-70% when the recurring plan is positioned on the first call."),
        ],
        "links": [("/pest-control-leads/", "Pest Control Lead Generation"),
                  ("/pest-control-marketing-guide/", "Pest Control Marketing Guide"),
                  ("/pay-per-call/", "Pay-Per-Call Lead Generation"),
                  ("/exclusive-vs-shared-leads/", "Exclusive vs Shared Leads")],
    },
    "Landscaping": {
        "lead_page": "/landscaping-leads/",
        "marketing_page": "/landscaping-marketing-guide/",
        "avg_job": "$800-8,000 (installation); $150-400/visit (maintenance)",
        "cpl": "$35-80",
        "close_rate": "25-40%",
        "services": "landscape installation, irrigation, lawn maintenance, and hardscaping",
        "bodies": [
            ("Landscaping splits into two business lines with fundamentally different economics: installation (high-ticket one-time projects) and maintenance (lower-ticket recurring visits that build predictable monthly revenue). The best landscaping contractors acquire installation customers through inbound calls and convert satisfied customers to recurring maintenance. Exclusive installation leads carry the highest immediate value; maintenance conversion creates the long-term base.",
             "Homeowners who call about landscaping have usually been thinking about the project for weeks or months. When they finally pick up the phone, they've set a rough budget and decided they're ready for estimates. That level of pre-qualification means the inbound landscaping call arrives with strong intent. Close rates run 25-40% for installation calls when estimates are delivered within 24 hours -- and a meaningful percentage of those installation customers convert to recurring maintenance."),
        ],
        "faqs": [
            ("How do exclusive landscaping leads work?",
             "Exclusive landscaping leads are inbound phone calls from homeowners seeking landscaping services in your area. You pay per qualified call over 60 seconds -- no competing landscapers receive the same contact."),
            ("What landscaping services generate the most calls?",
             "Landscape design and installation, irrigation installation and repair, lawn maintenance, sod installation, tree trimming, and hardscaping (patios, retaining walls) generate the highest call volumes."),
            ("What is the close rate on exclusive landscaping calls?",
             "Exclusive installation calls close at 25-40% when estimates are delivered within 24 hours. Maintenance calls close at 40-55% -- homeowners calling for recurring service have a specific ongoing need."),
        ],
        "links": [("/landscaping-leads/", "Landscaping Lead Generation"),
                  ("/landscaping-marketing-guide/", "Landscaping Marketing Guide"),
                  ("/pay-per-call/", "Pay-Per-Call Lead Generation"),
                  ("/exclusive-vs-shared-leads/", "Exclusive vs Shared Leads")],
    },
    "Fencing": {
        "lead_page": "/fence-leads/",
        "marketing_page": "/fence-contractor-marketing-guide/",
        "avg_job": "$2,000-8,000",
        "cpl": "$38-70",
        "close_rate": "25-35%",
        "services": "privacy fence installation, vinyl fence, wood fence, and aluminum ornamental",
        "bodies": [
            ("Fencing is a project-driven trade where homeowners arrive on the call knowing what they want -- they've decided on the yard to enclose, thought about the material, and they want to schedule an estimate. That clarity makes the inbound fence call efficient: the conversation is about timeline and pricing, not whether to proceed. Contractors who book the on-site estimate on the first call close at significantly higher rates than those who call back to schedule.",
             "Privacy fencing for suburban backyards is the highest-volume residential fence category in almost every market. New homeowners with kids or pets, homeowners replacing aging wood fences with vinyl, and homeowners adding property security all generate consistent call flow. Seasonal demand concentrates in spring and early summer in northern markets, while southern and southwestern states maintain near-year-round installation volume."),
        ],
        "faqs": [
            ("How do exclusive fence leads work?",
             "Exclusive fence leads are inbound phone calls from homeowners seeking fence installation or repair, delivered only to your business. You pay per qualified call over 60 seconds in your service area."),
            ("What fencing services generate the most calls?",
             "Privacy fence installation (wood and vinyl), aluminum ornamental, chain link, wood fence repair, and commercial fencing generate the highest call volumes."),
            ("What is the close rate on exclusive fence calls?",
             "Exclusive inbound fence calls close at 25-35% when on-site estimates are scheduled within 24-48 hours. Booking the estimate on the first call is the highest-impact close tactic."),
        ],
        "links": [("/fence-leads/", "Fence Lead Generation"),
                  ("/fence-contractor-marketing-guide/", "Fence Contractor Marketing Guide"),
                  ("/pay-per-call/", "Pay-Per-Call Lead Generation"),
                  ("/exclusive-vs-shared-leads/", "Exclusive vs Shared Leads")],
    },
    "Garage Door": {
        "lead_page": "/garage-door-repair-leads/",
        "marketing_page": "/garage-door-marketing-guide/",
        "avg_job": "$250-2,000 (repair); $1,500-4,000 (replacement)",
        "cpl": "$50-90",
        "close_rate": "35-50%",
        "services": "broken spring replacement, opener repair, panel replacement, and full door replacement",
        "bodies": [
            ("Garage door repair is one of the most urgent home service categories -- a broken spring or failed opener can trap a car inside the garage, preventing the homeowner from getting to work. That urgency means the homeowner who calls is not price-shopping or collecting estimates. They need it fixed today. Exclusive inbound garage door calls close at 35-50% when answered and same-day service is confirmed, making this category one of the highest-converting in residential home services.",
             "Emergency repair calls (broken springs, failed openers, cables off the drum) generate the highest daily volume in the garage door category. Replacement calls (homeowners upgrading to insulated doors, smart openers, or carriage-house styles) carry higher ticket values and slightly longer close cycles. Both categories perform well as exclusive inbound calls -- the urgency drives volume, and the replacement segment builds the high-ticket pipeline."),
        ],
        "faqs": [
            ("How do exclusive garage door leads work?",
             "Exclusive garage door leads are inbound phone calls from homeowners with active garage door issues. You pay per qualified call over 60 seconds in your service area -- no competing companies receive the same contact."),
            ("What garage door services generate the most calls?",
             "Broken spring replacement, opener repair and replacement, cable repair, panel replacement, and full door replacement and upgrade generate the highest call volumes."),
            ("What is the close rate on exclusive garage door calls?",
             "Exclusive inbound garage door calls close at 35-50%. Emergency repair calls close at 50%+ when same-day service is offered and confirmed on the initial call."),
        ],
        "links": [("/garage-door-repair-leads/", "Garage Door Repair Leads"),
                  ("/garage-door-marketing-guide/", "Garage Door Marketing Guide"),
                  ("/pay-per-call/", "Pay-Per-Call Lead Generation"),
                  ("/exclusive-vs-shared-leads/", "Exclusive vs Shared Leads")],
    },
    "Electrical": {
        "lead_page": "/electrical-leads/",
        "marketing_page": "/electrical-contractor-marketing-guide/",
        "avg_job": "$500-5,000",
        "cpl": "$45-95",
        "close_rate": "28-40%",
        "services": "panel upgrades, EV charger installation, electrical repair, and generator hookups",
        "bodies": [
            ("Electrical work is a licensed trade where homeowners almost universally hire professionals -- the safety stakes are too high and permits are required for most projects. That universal-hire dynamic means inbound electrical calls arrive with strong hiring intent. When a homeowner calls an electrician, they've already decided to hire; the conversation is about which electrician and when. Exclusive inbound calls remove the competing-contractor dynamic entirely.",
             "The fastest-growing electrical service categories reflect the electrification trend: EV charger installation (Level 2 home charging is now standard for EV owners), panel upgrades to accommodate new loads, and whole-home battery storage systems. These projects run $1,500-5,000+ and arrive with strong homeowner motivation. Emergency electrical calls (failed panels, circuit issues) provide year-round baseline volume on top of the growing project work."),
        ],
        "faqs": [
            ("How do exclusive electrical leads work?",
             "Exclusive electrical leads are inbound phone calls from homeowners seeking electrical services in your area. You pay per qualified call over 60 seconds -- no other electricians receive the same contact."),
            ("What electrical services generate the most calls?",
             "Panel upgrades, EV charger installation, emergency electrical repair, generator hookups, outlet and switch installation, and whole-home rewiring generate the highest call volumes."),
            ("What is the close rate on exclusive electrical calls?",
             "Exclusive inbound electrical calls close at 28-40% overall. Emergency calls close at the higher end; project calls (EV charger, panel upgrade) benefit from same-day or next-day estimate scheduling."),
        ],
        "links": [("/electrical-leads/", "Electrical Lead Generation"),
                  ("/electrical-contractor-marketing-guide/", "Electrical Contractor Marketing Guide"),
                  ("/pay-per-call/", "Pay-Per-Call Lead Generation"),
                  ("/exclusive-vs-shared-leads/", "Exclusive vs Shared Leads")],
    },
    "Painting": {
        "lead_page": "/painting-contractor-leads/",
        "marketing_page": "/painting-contractor-marketing-guide/",
        "avg_job": "$2,000-8,000",
        "cpl": "$35-65",
        "close_rate": "22-32%",
        "services": "exterior painting, interior painting, cabinet refinishing, and deck staining",
        "bodies": [
            ("Painting is a considered home improvement where homeowners accumulate motivation for weeks or months before calling. When they finally search for a painter and call, the decision to hire is already made -- they're in estimate-collection mode. That built-up intent makes inbound painting calls high-quality contacts who respond well to professional, same-day or next-day estimate follow-up. Close rates run 22-32% with prompt follow-up, which produces strong unit economics at average job values of $2,000-8,000.",
             "Exterior painting, interior whole-home repaints, and cabinet refinishing are the three highest-volume residential painting categories in most markets. Pre-sale painting projects carry strong urgency (homeowners listing often need painting completed in 2-3 weeks). Commercial painting for property management, offices, and retail adds a parallel high-value demand stream. Contractors who build inbound acquisition across both residential and commercial channels build more resilient businesses."),
        ],
        "faqs": [
            ("How do exclusive painting leads work?",
             "Exclusive painting leads are inbound phone calls from homeowners seeking painting services in your area. You pay per qualified call over 60 seconds -- no competing painters receive the same contact."),
            ("What painting services generate the most calls?",
             "Exterior house painting, interior whole-home painting, cabinet refinishing, deck staining, and commercial painting generate the highest call volumes."),
            ("What is the close rate on exclusive painting calls?",
             "Exclusive inbound painting calls close at 22-32% when estimates are delivered within 24-48 hours. Same-day or next-day estimate scheduling increases close rates meaningfully."),
        ],
        "links": [("/painting-contractor-leads/", "Painting Contractor Leads"),
                  ("/pay-per-call/", "Pay-Per-Call Lead Generation"),
                  ("/exclusive-vs-shared-leads/", "Exclusive vs Shared Leads"),
                  ("/contractor-leads/", "Contractor Lead Generation")],
    },
    "Window Replacement": {
        "lead_page": "/window-replacement-leads/",
        "marketing_page": "/window-replacement-marketing-guide/",
        "avg_job": "$3,000-15,000",
        "cpl": "$50-90",
        "close_rate": "20-30%",
        "services": "full window replacement, energy-efficient upgrades, impact windows, and sliding door replacement",
        "bodies": [
            ("Window replacement is a research-heavy home improvement category -- homeowners typically spend weeks comparing materials, styles, and energy efficiency ratings before calling contractors. By the time they make that call, they've decided to proceed; they're collecting estimates. That pre-qualification level makes inbound window calls high-intent contacts with strong average ticket values. Contractors who respond within hours and deliver professional estimates close at 20-30% with good follow-up.",
             "Energy efficiency is the primary value driver for window replacement in most markets -- homeowners motivated by high utility bills, drafty rooms, or aging single-pane windows respond strongly to energy savings messaging. Impact windows in Florida and Gulf Coast markets, noise-reduction windows in urban markets, and historic-style replacements in northeast markets represent significant regional demand. Exclusive inbound calls capture this intent when homeowner motivation is at its highest."),
        ],
        "faqs": [
            ("How do exclusive window replacement leads work?",
             "Exclusive window replacement leads are inbound phone calls from homeowners planning window installation or replacement. You pay per qualified call over 60 seconds in your service area."),
            ("What window services generate the most calls?",
             "Full window replacement, energy-efficient window upgrades, impact window installation (coastal markets), bay and bow windows, and sliding door replacement generate the highest volumes."),
            ("What is the close rate on exclusive window replacement calls?",
             "Exclusive inbound window calls close at 20-30% when estimates are delivered within 24-48 hours. The consideration cycle is longer than emergency trades, but average job values of $3,000-15,000 produce strong unit economics."),
        ],
        "links": [("/window-replacement-leads/", "Window Replacement Leads"),
                  ("/window-replacement-marketing-guide/", "Window Marketing Guide"),
                  ("/pay-per-call/", "Pay-Per-Call Lead Generation"),
                  ("/exclusive-vs-shared-leads/", "Exclusive vs Shared Leads")],
    },
    "Siding": {
        "lead_page": "/siding-leads/",
        "marketing_page": "/siding-contractor-marketing-guide/",
        "avg_job": "$6,000-18,000",
        "cpl": "$55-90",
        "close_rate": "20-30%",
        "services": "siding replacement, storm damage repair, fiber cement installation, and vinyl siding",
        "bodies": [
            ("Siding replacement is a high-ticket exterior project that homeowners often delay until the problem is undeniable -- rotting wood, cracking panels, or storm damage. When they finally search and call, they're motivated to move forward. Exclusive inbound calls from homeowners who searched for siding replacement deliver this high-intent audience to your estimating team, without the shared-lead competition dynamic that drives down close rates on marketplace platforms.",
             "Storm and hail damage is the single largest trigger for siding replacement in markets with active weather events. After a significant hail event, inbound calls spike as homeowners assess damage and begin the insurance process. Being positioned to handle that volume -- with a clear damage assessment process and insurance support -- turns storm season into the highest revenue window of the year for siding contractors in affected markets."),
        ],
        "faqs": [
            ("How do exclusive siding leads work?",
             "Exclusive siding leads are inbound phone calls from homeowners seeking siding replacement or repair. You pay per qualified call over 60 seconds -- no other siding contractors receive the same contact."),
            ("What siding services generate the most calls?",
             "Full siding replacement, storm damage assessment, fiber cement installation, vinyl siding upgrade, and rotted siding repair generate the highest call volumes."),
            ("What is the close rate on exclusive siding calls?",
             "Exclusive inbound siding calls close at 20-30% for full replacement projects. Storm damage calls close at higher rates when assessment and insurance claim support are included in the proposal."),
        ],
        "links": [("/siding-leads/", "Siding Lead Generation"),
                  ("/siding-contractor-marketing-guide/", "Siding Marketing Guide"),
                  ("/pay-per-call/", "Pay-Per-Call Lead Generation"),
                  ("/exclusive-vs-shared-leads/", "Exclusive vs Shared Leads")],
    },
    "Gutters": {
        "lead_page": "/gutter-leads/",
        "marketing_page": "/gutter-contractor-marketing-guide/",
        "avg_job": "$150-3,000",
        "cpl": "$28-65",
        "close_rate": "35-50%",
        "services": "gutter cleaning, gutter guard installation, gutter replacement, and downspout repair",
        "bodies": [
            ("Gutters are a seasonal but reliable home service category with two predictable demand peaks: fall cleaning as leaves drop, and spring repair after freeze-thaw damage. Gutter guard installation is the highest-ticket service in the category and creates a natural upsell from cleaning visits -- a homeowner paying for cleaning twice a year is the perfect candidate for a guard system that eliminates the need. The combination of cleaning volume and guard upsell creates strong lifetime customer value.",
             "Gutter replacement and guard installation have strong unit economics for contractors who focus on inbound acquisition. Full gutter replacement averages $1,500-3,000; guard systems add $1,000-3,000+ on top. The real business value is in the recurring cleaning customer who becomes a replacement and guard customer over 3-5 years. Exclusive inbound calls bring new customers into that lifecycle at the lowest cost per acquisition."),
        ],
        "faqs": [
            ("How do exclusive gutter leads work?",
             "Exclusive gutter leads are inbound phone calls from homeowners seeking gutter cleaning, repair, or replacement. You pay per qualified call over 60 seconds in your service area."),
            ("What gutter services generate the most calls?",
             "Gutter cleaning, gutter guard installation, full gutter replacement, clogged downspout repair, and fascia repair generate the highest call volumes."),
            ("What is the close rate on exclusive gutter calls?",
             "Exclusive inbound gutter calls close at 35-50% for cleaning and repair. Guard installation calls have slightly longer cycles but higher ticket values that produce strong ROI."),
        ],
        "links": [("/gutter-leads/", "Gutter Lead Generation"),
                  ("/gutter-contractor-marketing-guide/", "Gutter Marketing Guide"),
                  ("/pay-per-call/", "Pay-Per-Call Lead Generation"),
                  ("/exclusive-vs-shared-leads/", "Exclusive vs Shared Leads")],
    },
    "Pressure Washing": {
        "lead_page": "/pressure-washing-leads/",
        "marketing_page": "/pressure-washing-marketing-guide/",
        "avg_job": "$150-600",
        "cpl": "$25-50",
        "close_rate": "40-55%",
        "services": "house washing, driveway cleaning, roof soft washing, and deck cleaning",
        "bodies": [
            ("Pressure washing is a high-close-rate category because the homeowner's motivation is visual -- they looked at a dirty driveway or grimy house exterior one too many times and decided to call. That trigger means inbound intent is strong and close cycles are short. Homeowners who call about pressure washing typically hire on the same call when pricing is clear and scheduling is easy. Close rates run 40-55% on exclusive inbound calls when same-week availability is offered.",
             "Roof soft washing for algae and mildew removal is the highest-ticket pressure washing service in warm, humid markets -- and one of the most undersold. Homeowners don't always know to ask for it, but contractors who lead with roof wash offerings during house exterior calls regularly increase average ticket values by 40-60%. Building a recurring service program (annual driveway, biennial house wash) converts one-time inbound customers into predictable annual revenue."),
        ],
        "faqs": [
            ("How do exclusive pressure washing leads work?",
             "Exclusive pressure washing leads are inbound calls from homeowners or businesses seeking pressure washing services. You pay per qualified call over 60 seconds in your service area."),
            ("What pressure washing services generate the most calls?",
             "Driveway and sidewalk cleaning, house exterior washing, roof soft washing, deck and fence washing, and commercial property cleaning generate the highest volumes."),
            ("What is the close rate on exclusive pressure washing calls?",
             "Exclusive inbound pressure washing calls close at 40-55%. The short decision cycle means same-week scheduling availability is the primary close factor."),
        ],
        "links": [("/pressure-washing-leads/", "Pressure Washing Leads"),
                  ("/pressure-washing-marketing-guide/", "Pressure Washing Marketing Guide"),
                  ("/pay-per-call/", "Pay-Per-Call Lead Generation"),
                  ("/exclusive-vs-shared-leads/", "Exclusive vs Shared Leads")],
    },
    "Tree Service": {
        "lead_page": "/tree-service-leads/",
        "marketing_page": None,
        "avg_job": "$400-3,000",
        "cpl": "$40-80",
        "close_rate": "30-45%",
        "services": "tree removal, tree trimming, stump grinding, and emergency storm damage removal",
        "bodies": [
            ("Tree service is a category that combines emergency urgency (storm-damaged or hazard trees that need immediate removal) with planned project demand (routine trimming, dead tree removal, stump grinding). The emergency segment drives some of the highest close rates in residential home services -- a homeowner with a tree across their roof or a 60-foot dead oak threatening their house is not collecting estimates. They need it gone today. Exclusive inbound calls in this category close at 55-70% when same-day response is available.",
             "Certified arborist consultations, routine trimming, tree removal, and stump grinding are the four primary call categories in residential tree service. Commercial tree work for property management companies and municipalities adds higher-value projects with longer lead times. Exclusive inbound tree service calls are particularly valuable because homeowners who search and call for tree service have typically already determined that professional removal is necessary -- the conversation is about timeline and scope, not whether to hire."),
        ],
        "faqs": [
            ("How do exclusive tree service leads work?",
             "Exclusive tree service leads are inbound phone calls from homeowners needing tree removal, trimming, or stump grinding. You pay per qualified call over 60 seconds in your service area."),
            ("What tree services generate the most calls?",
             "Emergency tree removal (storm damage, hazard trees), routine tree trimming, dead tree removal, stump grinding, and arborist assessments generate the highest call volumes."),
            ("What is the close rate on exclusive tree service calls?",
             "Exclusive inbound tree service calls close at 30-45% overall. Emergency removal calls (tree on structure, imminent hazard) close at 55-70% when same-day or next-day response is available."),
        ],
        "links": [("/contractor-leads/", "Contractor Lead Generation"),
                  ("/pay-per-call/", "Pay-Per-Call Lead Generation"),
                  ("/exclusive-vs-shared-leads/", "Exclusive vs Shared Leads"),
                  ("/seasonal-demand-for-contractors/", "Seasonal Demand for Contractors")],
    },
    "Insulation": {
        "lead_page": "/insulation-leads/",
        "marketing_page": None,
        "avg_job": "$1,500-6,000",
        "cpl": "$45-80",
        "close_rate": "25-35%",
        "services": "attic insulation, spray foam, blown-in insulation, and crawl space encapsulation",
        "bodies": [
            ("Insulation has strong and growing demand driven by high energy costs, aging housing stock with inadequate insulation, and increasing homeowner awareness of efficiency incentives. Homeowners who call about insulation are motivated by one of three things: high utility bills, an energy audit that flagged inadequate insulation, or a renovation that exposed old or missing material. Each of these motivations produces a high-intent lead who is ready to schedule an assessment and move forward.",
             "Attic insulation removal and replacement and spray foam for crawl spaces and rim joists are the two highest-ticket residential insulation categories. Air sealing paired with insulation increases average job values and improves energy results significantly. Many states offer utility rebates for insulation upgrades, which strengthens the homeowner ROI case and improves close rates when the rebate conversation is handled well on the initial call."),
        ],
        "faqs": [
            ("How do exclusive insulation leads work?",
             "Exclusive insulation leads are inbound phone calls from homeowners seeking insulation installation or upgrades. You pay per qualified call over 60 seconds in your service area."),
            ("What insulation services generate the most calls?",
             "Attic insulation installation and removal, spray foam insulation, blown-in insulation for existing walls, crawl space encapsulation, and air sealing generate the highest call volumes."),
            ("What is the close rate on exclusive insulation calls?",
             "Exclusive inbound insulation calls close at 25-35% when an assessment is offered on the first call and the rebate/financing discussion is included in the conversation."),
        ],
        "links": [("/contractor-leads/", "Contractor Lead Generation"),
                  ("/pay-per-call/", "Pay-Per-Call Lead Generation"),
                  ("/exclusive-vs-shared-leads/", "Exclusive vs Shared Leads"),
                  ("/contractor-lead-roi-guide/", "Contractor Lead ROI Guide")],
    },
}

# ── STATE DATA ───────────────────────────────────────────────────────────────

STATE_DATA = {
    "Arizona": {
        "abbr": "AZ", "cities": "Phoenix, Tucson, Scottsdale, Mesa, and Chandler",
        "climate": "extreme desert heat (110+ degree summers) and low humidity",
        "market": "rapidly growing population with one of the highest new construction rates in the country",
        "seasonal": "HVAC demand peaks June-September; exterior trades peak October-May avoiding summer heat",
    },
    "Georgia": {
        "abbr": "GA", "cities": "Atlanta, Savannah, Augusta, Columbus, and Macon",
        "climate": "warm, humid climate with active spring and summer storm season",
        "market": "rapid suburban expansion around Atlanta metro drives strong residential contractor demand across all trades",
        "seasonal": "year-round demand with peaks in spring and early summer",
    },
    "North Carolina": {
        "abbr": "NC", "cities": "Charlotte, Raleigh, Durham, Greensboro, and Winston-Salem",
        "climate": "mild climate with active hurricane and severe storm season; coastal markets have significant weather exposure",
        "market": "one of the fastest-growing states in the US with strong residential construction and renovation demand",
        "seasonal": "spring through fall for most exterior trades; year-round for HVAC and emergency services",
    },
    "Colorado": {
        "abbr": "CO", "cities": "Denver, Colorado Springs, Aurora, Fort Collins, and Boulder",
        "climate": "cold winters with significant snowfall at elevation and active spring hail season along the Front Range",
        "market": "growing Front Range population with strong home renovation demand; hail is a major roofing and siding driver",
        "seasonal": "spring hail season (roofing/siding), summer construction peak, pre-winter HVAC and insulation demand",
    },
    "Illinois": {
        "abbr": "IL", "cities": "Chicago, Aurora, Naperville, Rockford, and Joliet",
        "climate": "cold winters and hot summers creating year-round HVAC demand; freeze-thaw cycles create roofing and plumbing urgency",
        "market": "Chicago metro is one of the largest home services markets in the Midwest with consistent demand across all trades",
        "seasonal": "spring through fall for outdoor trades; winter for HVAC emergency and plumbing",
    },
    "Virginia": {
        "abbr": "VA", "cities": "Virginia Beach, Norfolk, Richmond, Arlington, and Chesapeake",
        "climate": "mid-Atlantic climate with hot summers and cold winters; coastal markets have hurricane exposure",
        "market": "Northern Virginia DC-area suburbs are among the highest-value home renovation markets in the country",
        "seasonal": "spring through fall for outdoor trades; year-round for HVAC and emergency services",
    },
    "Washington": {
        "abbr": "WA", "cities": "Seattle, Spokane, Tacoma, Bellevue, and Everett",
        "climate": "wet Pacific Northwest climate with significant rainfall; moss and moisture issues are major drivers for roofing and exterior trades",
        "market": "Seattle metro is one of the most active home renovation markets in the Pacific Northwest",
        "seasonal": "spring and summer for outdoor trades (compressed season); year-round for interior trades",
    },
    "Nevada": {
        "abbr": "NV", "cities": "Las Vegas, Henderson, Reno, North Las Vegas, and Sparks",
        "climate": "desert climate with extreme summer heat in Las Vegas (115+ degree days) driving very high HVAC demand",
        "market": "Las Vegas metro is a high-growth market with active new construction and consistent renovation demand",
        "seasonal": "year-round for HVAC and interior; spring and fall for exterior trades avoiding extreme heat",
    },
    "New York": {
        "abbr": "NY", "cities": "New York City, Buffalo, Rochester, Yonkers, and Syracuse",
        "climate": "cold winters with significant snowfall create strong heating demand; ice dams are a major roofing issue in western NY",
        "market": "New York metro and Long Island are among the highest-value home services markets in the country with very high labor costs",
        "seasonal": "spring through fall for outdoor trades; year-round for HVAC, plumbing emergency, and interior renovation",
    },
    "Pennsylvania": {
        "abbr": "PA", "cities": "Philadelphia, Pittsburgh, Allentown, Erie, and Reading",
        "climate": "four-season climate with cold winters and warm summers; older housing stock creates significant repair and replacement demand",
        "market": "Philadelphia and Pittsburgh metros are active home services markets; older homes statewide generate consistent renovation demand",
        "seasonal": "spring through fall for outdoor trades; winter for HVAC and emergency plumbing",
    },
    "Tennessee": {
        "abbr": "TN", "cities": "Nashville, Memphis, Knoxville, Chattanooga, and Clarksville",
        "climate": "warm climate with active spring storm and tornado season; occasional winter ice events",
        "market": "Nashville metro is one of the fastest-growing real estate markets in the Southeast, driving strong contractor demand",
        "seasonal": "spring through fall with strong year-round interior demand; storm season creates roofing demand spikes",
    },
    "South Carolina": {
        "abbr": "SC", "cities": "Columbia, Charleston, North Charleston, Greenville, and Myrtle Beach",
        "climate": "warm, humid climate with active hurricane season; coastal markets have significant storm and wind exposure",
        "market": "Charleston coastal market and Greenville inland market have seen significant growth with active renovation demand",
        "seasonal": "year-round demand with summer outdoor peak; hurricane season (June-November) creates roofing and siding demand spikes",
    },
    "Maryland": {
        "abbr": "MD", "cities": "Baltimore, Silver Spring, Columbia, Rockville, and Germantown",
        "climate": "mid-Atlantic climate with hot humid summers and cold winters; Baltimore and DC suburbs have significant older housing stock",
        "market": "DC suburbs (Montgomery County, Prince George's County) are among the highest-value home renovation markets on the East Coast",
        "seasonal": "spring through fall for outdoor trades; year-round for HVAC and interior services",
    },
    "Massachusetts": {
        "abbr": "MA", "cities": "Boston, Worcester, Springfield, Cambridge, and Lowell",
        "climate": "New England winters with snow and ice create ice dam and heating demand; short but active outdoor season",
        "market": "Boston metro is one of the highest-cost and highest-value home services markets in the country; older housing stock drives renovation demand",
        "seasonal": "spring through fall for outdoor trades; winter for heating, emergency plumbing, and ice dam roofing calls",
    },
    "Minnesota": {
        "abbr": "MN", "cities": "Minneapolis, Saint Paul, Rochester, Duluth, and Bloomington",
        "climate": "extreme winters create strong heating, roofing (ice dams), and insulation demand; compressed outdoor season May-September",
        "market": "Twin Cities metro has consistent home renovation demand; extreme weather creates year-round emergency service call volume",
        "seasonal": "May-September for outdoor trades; winter for heating, insulation, and roofing emergency calls",
    },
    "Missouri": {
        "abbr": "MO", "cities": "Kansas City, Saint Louis, Springfield, Independence, and Columbia",
        "climate": "Midwest climate with cold winters and hot summers; tornado and severe storm season creates roofing demand in spring",
        "market": "Kansas City and Saint Louis are established Midwest home services markets with consistent demand across all trades",
        "seasonal": "spring storm season (roofing demand spike), summer outdoor peak, fall pre-winter service calls",
    },
    "Ohio": {
        "abbr": "OH", "cities": "Columbus, Cleveland, Cincinnati, Akron, and Dayton",
        "climate": "four-season Midwest climate with cold winters; freeze-thaw cycles create consistent plumbing and roofing demand",
        "market": "Columbus, Cleveland, and Cincinnati are active markets with strong residential renovation demand across all trades",
        "seasonal": "spring through fall for outdoor trades; winter for HVAC emergency and plumbing",
    },
    "Michigan": {
        "abbr": "MI", "cities": "Detroit, Grand Rapids, Lansing, Ann Arbor, and Flint",
        "climate": "cold winters with significant lake-effect snow; freeze-thaw damage drives spring repair demand across multiple trades",
        "market": "Detroit metro and Grand Rapids are active home services markets; older housing stock drives consistent renovation demand",
        "seasonal": "spring through fall for outdoor trades; winter for HVAC, plumbing emergency, and post-winter repair calls",
    },
    "Oregon": {
        "abbr": "OR", "cities": "Portland, Salem, Eugene, Gresham, and Hillsboro",
        "climate": "wet Pacific Northwest climate with heavy rainfall and mild temperatures; moss, mold, and moisture issues are major drivers for roofing, siding, and exterior trades",
        "market": "Portland metro is one of the fastest-growing Pacific Northwest markets with strong demand for home renovation and contractor services",
        "seasonal": "compressed outdoor season (May-September) due to heavy rain; year-round demand for interior trades and emergency services",
    },
    "Indiana": {
        "abbr": "IN", "cities": "Indianapolis, Fort Wayne, Evansville, South Bend, and Carmel",
        "climate": "Midwest four-season climate with cold winters and hot summers; tornado and severe storm season creates roofing demand spikes in spring",
        "market": "Indianapolis metro is a growing Midwest market with strong residential construction and consistent renovation demand across all trades",
        "seasonal": "spring through fall for outdoor trades; winter for HVAC and emergency plumbing; spring storm season drives roofing demand",
    },
    "Wisconsin": {
        "abbr": "WI", "cities": "Milwaukee, Madison, Green Bay, Kenosha, and Racine",
        "climate": "cold winters with significant snowfall; freeze-thaw cycles create consistent roofing, plumbing, and foundation demand each spring",
        "market": "Milwaukee and Madison are established Wisconsin home services markets; older housing stock statewide drives consistent renovation and repair demand",
        "seasonal": "May-September for outdoor trades; winter for HVAC, insulation, and heating emergency calls",
    },
    "Louisiana": {
        "abbr": "LA", "cities": "New Orleans, Baton Rouge, Shreveport, Metairie, and Lafayette",
        "climate": "hot, humid subtropical climate with active hurricane season; heat, humidity, and storm exposure drive HVAC, roofing, and pest control demand year-round",
        "market": "New Orleans metro and Baton Rouge are active home services markets; hurricane recovery creates significant roofing and siding demand after storm events",
        "seasonal": "year-round demand with HVAC peaks in summer and roofing demand spikes following hurricane and tropical storm events",
    },
    "Alabama": {
        "abbr": "AL", "cities": "Birmingham, Montgomery, Huntsville, Mobile, and Tuscaloosa",
        "climate": "warm, humid climate with active tornado and severe storm season; storm damage is a major roofing and siding demand driver",
        "market": "Huntsville is one of the fastest-growing markets in the Southeast; Birmingham remains the largest home services market in the state",
        "seasonal": "year-round demand with spring storm season peaks and hot summers driving HVAC demand",
    },
    "Kentucky": {
        "abbr": "KY", "cities": "Louisville, Lexington, Bowling Green, Owensboro, and Covington",
        "climate": "four-season climate with cold winters, hot summers, and active spring storm season; ice storms create periodic emergency service demand",
        "market": "Louisville metro is the dominant home services market; Lexington and the Northern Kentucky Cincinnati suburbs generate consistent renovation demand",
        "seasonal": "spring through fall for outdoor trades; winter for HVAC and plumbing emergency; spring storm season drives roofing demand",
    },
    "Iowa": {
        "abbr": "IA", "cities": "Des Moines, Cedar Rapids, Davenport, Sioux City, and Iowa City",
        "climate": "continental Midwest climate with cold winters and hot summers; severe spring storm season produces hail and wind damage driving roofing demand",
        "market": "Des Moines is the primary home services market; aging housing stock across Iowa creates consistent repair and replacement demand for all trades",
        "seasonal": "spring through fall for outdoor trades; winter for HVAC and emergency plumbing; spring hail season drives roofing demand",
    },
    "Kansas": {
        "abbr": "KS", "cities": "Wichita, Overland Park, Kansas City, Olathe, and Topeka",
        "climate": "Great Plains climate with extreme weather variability; hail, tornadoes, and high winds create significant roofing and siding demand seasonally",
        "market": "Kansas City metro (including Overland Park and Olathe) is the dominant home services market with strong suburban renovation demand",
        "seasonal": "spring storm and tornado season drives roofing demand; summer HVAC peaks; year-round interior trades",
    },
    "Oklahoma": {
        "abbr": "OK", "cities": "Oklahoma City, Tulsa, Norman, Broken Arrow, and Lawton",
        "climate": "severe weather state with frequent tornadoes, hail, and high winds; Oklahoma is one of the highest roofing demand states per capita due to storm frequency",
        "market": "Oklahoma City and Tulsa are active home services markets; storm damage recovery creates consistent high-volume roofing and siding call flow",
        "seasonal": "spring tornado and hail season creates roofing demand spikes; summer HVAC peaks; year-round interior and emergency services",
    },
    "Utah": {
        "abbr": "UT", "cities": "Salt Lake City, West Valley City, Provo, West Jordan, and Orem",
        "climate": "semi-arid climate with cold mountain winters and hot summers; the Wasatch Front experiences significant snowfall and freeze-thaw cycles",
        "market": "Salt Lake City metro is one of the fastest-growing markets in the Mountain West with active new construction and strong renovation demand",
        "seasonal": "spring through fall for outdoor trades; winter for HVAC and insulation; year-round interior demand in the growing Salt Lake metro",
    },
    "Connecticut": {
        "abbr": "CT", "cities": "Bridgeport, New Haven, Stamford, Hartford, and Waterbury",
        "climate": "New England climate with cold winters and nor'easters; older housing stock is a major driver of renovation and replacement demand across all trades",
        "market": "Fairfield County (Stamford area) is one of the highest-income home services markets in the Northeast; Hartford and New Haven generate consistent renovation demand",
        "seasonal": "spring through fall for outdoor trades; winter for heating, emergency plumbing, and ice dam roofing calls",
    },
    "New Jersey": {
        "abbr": "NJ", "cities": "Newark, Jersey City, Paterson, Elizabeth, and Trenton",
        "climate": "mid-Atlantic climate with cold winters and hot summers; coastal markets have hurricane and nor'easter exposure",
        "market": "New Jersey has some of the highest home values in the country; suburban markets in Morris, Bergen, and Monmouth counties generate premium renovation demand",
        "seasonal": "spring through fall for outdoor trades; winter for HVAC and emergency plumbing; year-round interior renovation demand",
    },
    "Arkansas": {
        "abbr": "AR", "cities": "Little Rock, Fort Smith, Fayetteville, Springdale, and Jonesboro",
        "climate": "warm, humid climate with active spring tornado and storm season; ice storms in winter create periodic emergency service demand",
        "market": "Fayetteville and the Northwest Arkansas corridor are among the fastest-growing markets in the South; Little Rock is the primary established home services market",
        "seasonal": "spring through fall with storm season peaks; HVAC demand in hot summers; year-round interior trades",
    },
    "Mississippi": {
        "abbr": "MS", "cities": "Jackson, Gulfport, Southaven, Hattiesburg, and Biloxi",
        "climate": "hot, humid subtropical climate with active hurricane season; coastal markets have significant storm exposure and Gulf Coast weather damage patterns",
        "market": "Jackson metro and Gulf Coast markets generate consistent home services demand; hurricane recovery creates periodic high-volume roofing and siding demand",
        "seasonal": "year-round demand with summer HVAC peaks; hurricane season (June-November) creates roofing and siding demand spikes in coastal markets",
    },
    "New Mexico": {
        "abbr": "NM", "cities": "Albuquerque, Las Cruces, Rio Rancho, Santa Fe, and Roswell",
        "climate": "high-desert climate with extreme temperature swings; Albuquerque experiences cold winters, hot summers, and monsoon season moisture that drives roofing and HVAC demand",
        "market": "Albuquerque metro is the dominant home services market; Rio Rancho is one of the fastest-growing suburban markets in the Southwest",
        "seasonal": "year-round HVAC demand due to temperature extremes; spring and fall for exterior trades; monsoon season (July-September) drives roofing and drainage calls",
    },
    "Idaho": {
        "abbr": "ID", "cities": "Boise, Nampa, Meridian, Idaho Falls, and Caldwell",
        "climate": "semi-arid climate with cold winters; the Treasure Valley (Boise area) has experienced rapid growth with strong residential construction activity",
        "market": "Boise metro is one of the fastest-growing markets in the Mountain West with very high new construction rates and growing renovation demand",
        "seasonal": "spring through fall for outdoor trades; winter for HVAC and insulation; year-round demand in the rapidly growing Boise metro",
    },
    "Nebraska": {
        "abbr": "NE", "cities": "Omaha, Lincoln, Bellevue, Grand Island, and Kearney",
        "climate": "Great Plains climate with cold winters, hot summers, and active spring storm season; hail and high winds drive roofing and siding demand",
        "market": "Omaha metro is the dominant home services market with consistent residential renovation demand; Lincoln generates solid secondary market activity",
        "seasonal": "spring through fall for outdoor trades; spring hail season drives roofing demand; winter for HVAC and emergency plumbing",
    },
    "West Virginia": {
        "abbr": "WV", "cities": "Charleston, Huntington, Morgantown, Parkersburg, and Wheeling",
        "climate": "Appalachian climate with cold winters, significant snowfall in elevated areas, and active freeze-thaw cycles that create consistent plumbing and roofing demand",
        "market": "aging housing stock is the primary driver of home services demand; renovation and replacement work is consistent across all major metro areas",
        "seasonal": "spring through fall for outdoor trades; winter for HVAC emergency and plumbing; spring for post-winter repair demand",
    },
    "Maine": {
        "abbr": "ME", "cities": "Portland, Lewiston, Bangor, South Portland, and Auburn",
        "climate": "harsh New England winters with heavy snowfall; very short outdoor season from May to September; heating, insulation, and roofing are year-round demand categories",
        "market": "Portland metro is the primary home services market; Maine has a significant vacation and second-home market that drives seasonal renovation demand",
        "seasonal": "May-September for outdoor trades (very compressed); winter is the primary season for heating, insulation, and indoor renovation calls",
    },
    "Hawaii": {
        "abbr": "HI", "cities": "Honolulu, Pearl City, Hilo, Kailua, and Kapolei",
        "climate": "tropical climate with high humidity, salt air exposure, and heavy rainfall on windward coasts; moisture damage, roof replacement, and pest control are primary demand drivers",
        "market": "Honolulu metro is one of the highest-cost home services markets in the country; Oahu and Maui generate strong demand for roofing, painting, and pest control",
        "seasonal": "year-round demand across all trades; rainy season (November-March on windward coasts) drives roofing and waterproofing calls",
    },
}

# ── CONTENT GENERATION ───────────────────────────────────────────────────────

def _variant(slug, n):
    """Pick a consistent variant index for a given slug."""
    return int(hashlib.md5(slug.encode()).hexdigest(), 16) % n


def make_service_page(topic):
    """Generate a full page dict for a service (geo x trade) topic."""
    trade  = topic["trade"]
    state  = topic["state"]
    slug   = topic["slug"]

    td = TRADE_DATA.get(trade, {})
    sd = STATE_DATA.get(state, {})

    cities   = sd.get("cities", state)
    climate  = sd.get("climate", "active home services market")
    market   = sd.get("market", "strong residential demand")
    seasonal = sd.get("seasonal", "year-round demand")
    avg_job  = td.get("avg_job", "$500-5,000")
    cpl      = td.get("cpl", "$50-90")
    close    = td.get("close_rate", "25-35%")
    services = td.get("services", trade.lower() + " services")

    bodies = td.get("bodies", [("",)])
    body_idx = _variant(slug, len(bodies))
    body_main = bodies[body_idx][_variant(slug + "b", len(bodies[body_idx]))]

    state_para = (
        state + " is an active market for " + trade.lower() + " services, shaped by "
        + climate + ". " + market + ". Major "
        + trade.lower() + " markets in " + state + " include " + cities + ". "
        + "Demand is " + seasonal + ". "
        + "RankLocal delivers exclusive " + trade.lower() + " leads in " + state
        + " as inbound phone calls -- you pay only for qualified calls over 60 seconds"
        + " from within your " + state + " service area."
        + " Average call cost: " + cpl + " per qualified call."
        + " Close rate on exclusive calls: " + close + "."
    )

    full_body = "<p>" + body_main + "</p><p>" + state_para + "</p>"

    # FAQs
    base_faqs = td.get("faqs", [])
    faqs = [{"q": q, "a": a} for q, a in base_faqs]
    faqs.append({
        "q": "What " + trade.lower() + " services are most in demand in " + state + "?",
        "a": (state + " homeowners most frequently call for " + services + ". "
              + "Demand is " + seasonal + ".")
    })

    title = (trade + " Leads in " + state
             + " | Exclusive Inbound Calls for " + state + " " + trade + " Contractors")
    h1    = "Exclusive " + trade + " Leads in " + state
    meta  = ("Get exclusive " + trade.lower() + " leads in " + state
             + ". Inbound calls from " + state + " homeowners needing "
             + trade.lower() + " services. Pay per qualified call.")
    hero_sub = ("Exclusive inbound calls from " + state
                + " homeowners. No shared leads, no monthly minimums.")

    related = td.get("links", [])
    links = [{"href": h, "text": t} for h, t in related]
    links.append({"href": "/contractor-leads/", "text": "Contractor Lead Generation"})
    links.append({"href": "/apply/", "text": "Apply Now"})

    return {
        "slug": slug, "type": "service",
        "title": title, "h1": h1, "meta": meta,
        "hero_sub": hero_sub, "trade": trade,
        "body": full_body, "faq": faqs, "links": links,
    }


# ── SCHEMA BUILDERS ──────────────────────────────────────────────────────────

def make_service_schema(p):
    url = SITE + "/" + p["slug"] + "/"
    schema = [
        {"@type": "Service",
         "name": p["h1"],
         "description": p["meta"],
         "provider": {"@type": "Organization", "name": "RankLocal",
                      "url": SITE},
         "areaServed": p.get("trade", ""),
         "url": url},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1,
             "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2,
             "name": p["h1"], "item": url},
        ]},
        PERSON_SCHEMA,
    ]
    if p.get("faq"):
        schema.append({
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": fq["q"],
                 "acceptedAnswer": {"@type": "Answer", "text": fq["a"]}}
                for fq in p["faq"]
            ]
        })
    return json.dumps({"@context": "https://schema.org", "@graph": schema},
                      ensure_ascii=False)


# ── HTML RENDERERS ───────────────────────────────────────────────────────────

def render_service(p):
    schema_str = make_service_schema(p)
    faq_html = ""
    for fq in p.get("faq", []):
        faq_html += ("<div class='faq-item'>"
                     "<h3>" + fq["q"] + "</h3>"
                     "<p>" + fq["a"] + "</p>"
                     "</div>")
    links_html = ""
    for lk in p.get("links", []):
        links_html += "<li><a href='" + lk["href"] + "'>" + lk["text"] + "</a></li>"

    html = ("<!DOCTYPE html><html lang='en'>"
            "<head><meta charset='UTF-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>" + p["title"] + " | RankLocal</title>"
            "<meta name='description' content='" + p["meta"].replace("'", "&#39;") + "'>"
            "<link rel='stylesheet' href='/assets/css/style.css'>"
            "<link rel='icon' href='/favicon.ico'>"
            "<script type='application/ld+json'>" + schema_str + "</script>"
            "</head><body>"
            "<header class='site-header'>" + NAV + "</header>"
            "<section class='hero hero-service'>"
            "<div class='hero-inner'>"
            "<h1>" + p["h1"] + "</h1>"
            "<p class='hero-sub'>" + p.get("hero_sub", "") + "</p>"
            "<a href='/apply/' class='cta-btn cta-hero'>Apply Now &rarr;</a>"
            "</div></section>"
            "<main class='container'>"
            "<article class='content-article'>"
            "<p class='byline'>" + BYLINE + "</p>"
            + p.get("body", "") +
            "</article>"
            "<section class='faq-section'>"
            "<h2>Frequently Asked Questions</h2>"
            + faq_html +
            "</section>"
            "<section class='related-links'>"
            "<h2>Related Resources</h2><ul>"
            + links_html +
            "</ul></section>"
            "<section class='cta-section'>"
            "<h2>Ready to Get Exclusive " + p.get("trade", "") + " Leads?</h2>"
            "<p>Apply now and start receiving exclusive inbound calls in your service area.</p>"
            "<a href='/apply/' class='cta-btn'>Apply Now</a>"
            "</section>"
            "</main>"
            + FOOTER +
            "</body></html>")
    return html


def render_article(p):
    schema_items = [
        {"@type": "Article",
         "headline": p["h1"],
         "description": p["meta"],
         "author": PERSON_SCHEMA,
         "publisher": {"@type": "Organization", "name": "RankLocal",
                       "url": SITE},
         "url": SITE + "/" + p["slug"] + "/",
         "dateModified": _now.strftime("%Y-%m-%d")},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1,
             "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2,
             "name": p["h1"], "item": SITE + "/" + p["slug"] + "/"},
        ]},
        PERSON_SCHEMA,
    ]
    if p.get("faq"):
        schema_items.append({
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": fq["q"],
                 "acceptedAnswer": {"@type": "Answer", "text": fq["a"]}}
                for fq in p["faq"]
            ]
        })
    schema_str = json.dumps({"@context": "https://schema.org",
                             "@graph": schema_items}, ensure_ascii=False)

    faq_html = ""
    for fq in p.get("faq", []):
        faq_html += ("<div class='faq-item'>"
                     "<h3>" + fq["q"] + "</h3>"
                     "<p>" + fq["a"] + "</p>"
                     "</div>")
    links_html = ""
    for lk in p.get("links", []):
        links_html += "<li><a href='" + lk["href"] + "'>" + lk["text"] + "</a></li>"

    html = ("<!DOCTYPE html><html lang='en'>"
            "<head><meta charset='UTF-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>" + p["title"] + " | RankLocal</title>"
            "<meta name='description' content='" + p["meta"].replace("'", "&#39;") + "'>"
            "<link rel='stylesheet' href='/assets/css/style.css'>"
            "<link rel='icon' href='/favicon.ico'>"
            "<script type='application/ld+json'>" + schema_str + "</script>"
            "</head><body>"
            "<header class='site-header'>" + NAV + "</header>"
            "<main class='container content-article'>"
            "<h1>" + p["h1"] + "</h1>"
            "<p class='byline'>" + BYLINE + "</p>"
            + p.get("body", "") +
            "<section class='faq-section'>"
            "<h2>Frequently Asked Questions</h2>"
            + faq_html +
            "</section>"
            "<section class='related-links'>"
            "<h2>Related Resources</h2><ul>"
            + links_html +
            "</ul></section>"
            "<section class='cta-section'>"
            "<p>Ready to get exclusive inbound contractor leads?</p>"
            "<a href='/apply/' class='cta-btn'>Apply Now</a>"
            "</section>"
            "</main>"
            + FOOTER +
            "</body></html>")
    return html


# ── SITEMAP + YML ────────────────────────────────────────────────────────────

def update_sitemap(slugs):
    if not os.path.exists(SITEMAP):
        return 0
    with open(SITEMAP, "r", encoding="utf-8") as f:
        content = f.read()
    today = _now.strftime("%Y-%m-%d")
    blocks = ""
    added = 0
    for slug in slugs:
        url = SITE + "/" + slug + "/"
        if url not in content:
            blocks += ("\n  <url>\n"
                       "    <loc>" + url + "</loc>\n"
                       "    <lastmod>" + today + "</lastmod>\n"
                       "    <changefreq>monthly</changefreq>\n"
                       "    <priority>0.7</priority>\n"
                       "  </url>")
            added += 1
    if blocks:
        content = content.replace("</urlset>", blocks + "\n</urlset>")
        with open(SITEMAP, "w", encoding="utf-8") as f:
            f.write(content)
    return added


def update_yml(slugs):
    if not os.path.exists(YML_PATH):
        return 0
    with open(YML_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    added = 0
    insert_lines = ""
    for slug in slugs:
        url = '"' + SITE + "/" + slug + '/"'
        if url not in content:
            insert_lines += "            " + url + ",\n"
            added += 1
    if insert_lines and "]}" + ")" in content:
        content = content.replace("]}" + ")", insert_lines + "          ]}" + ")")
        # Update count
        import re
        existing = len(re.findall(r'"https://ranklocall\.com/', content))
        content = re.sub(r'(urls\s*\(\s*count\s*=\s*)\d+',
                         r'\g<1>' + str(existing), content)
        with open(YML_PATH, "w", encoding="utf-8") as f:
            f.write(content)
    return added


# ── GIT + DEPLOY ─────────────────────────────────────────────────────────────

def git_push(week_label, count):
    msg = "Weekly SEO batch " + week_label + ": " + str(count) + " new pages"
    cmds = [
        "git -C " + BASE + " add -A",
        'git -C ' + BASE + ' commit -m "' + msg + '"',
        "git -C " + BASE + " push origin main",
    ]
    for cmd in cmds:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print("GIT ERROR: " + result.stderr.strip())
            return False
    return True


def ping_google():
    sitemap_url = SITE + "/sitemap.xml"
    ping_url = ("https://www.google.com/ping?sitemap="
                + urllib.request.quote(sitemap_url, safe=""))
    try:
        with urllib.request.urlopen(ping_url, timeout=10) as r:
            return r.status == 200
    except Exception:
        return False


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    log_lines = []

    def log(msg):
        print(msg)
        log_lines.append(msg)

    log("=== weekly_seo_batch.py === " + _now.strftime("%Y-%m-%d %H:%M"))

    # 1. Load queue
    if not os.path.exists(QUEUE_PATH):
        log("ERROR: topic_queue.json not found at " + QUEUE_PATH)
        sys.exit(1)
    with open(QUEUE_PATH, "r", encoding="utf-8") as f:
        queue = json.load(f)

    pending = [t for t in queue if t.get("status") == "pending"]
    batch   = pending[:BATCH_SIZE]
    log("Queue: " + str(len(pending)) + " pending topics. Processing " + str(len(batch)) + ".")

    if not batch:
        log("No pending topics in queue. Add more to topic_queue.json to continue.")
        return

    # 2. Generate pages
    written = 0
    skipped = 0
    new_slugs = []
    week_label = _now.strftime("%Y-W%V")

    for topic in batch:
        slug = topic["slug"]
        dest = os.path.join(BASE, slug, "index.html")

        if os.path.exists(dest):
            log("[SKIP] " + slug + " (already exists)")
            skipped += 1
            topic["status"] = "done"
            continue

        # Generate page object
        if topic.get("type") == "service":
            page = make_service_page(topic)
        else:
            log("[SKIP] " + slug + " (article type - add to pages_batch4.json)")
            topic["status"] = "pending"
            continue

        # Write HTML
        os.makedirs(os.path.join(BASE, slug), exist_ok=True)
        html = render_service(page)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(html)

        log("[OK] " + slug)
        topic["status"] = "done"
        new_slugs.append(slug)
        written += 1

    # 3. Update sitemap + YML
    if new_slugs:
        sm = update_sitemap(new_slugs)
        ym = update_yml(new_slugs)
        log("Sitemap: " + str(sm) + " URLs added. YML: " + str(ym) + " URLs added.")

    # 4. Save updated queue
    with open(QUEUE_PATH, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)

    # 5. Git push
    if new_slugs:
        ok = git_push(week_label, written)
        log("Git push: " + ("OK" if ok else "FAILED"))

        # 6. Ping Google
        pinged = ping_google()
        log("Google ping: " + ("OK" if pinged else "skipped/failed"))
    else:
        log("No new pages to deploy.")

    remaining = len([t for t in queue if t.get("status") == "pending"])
    log("Done. Written: " + str(written) + " | Skipped: " + str(skipped)
        + " | Queue remaining: " + str(remaining))

    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write("\n".join(log_lines) + "\n\n")


if __name__ == "__main__":
    main()
