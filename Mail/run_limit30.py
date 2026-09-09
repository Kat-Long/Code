# -*- coding: utf-8 -*-
import extract_final

s = extract_final.Scraper()
s.run()
s.enrich_profiles(limit=30)
s.save()