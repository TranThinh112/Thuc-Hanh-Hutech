# -*- coding: utf-8 -*-
import os, sys, re, json

with open('python_app/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix line 859 bug
old_cond = 'if requested_device and "hacker" in requested_device or "script" in requested_device or "foreign" in requested_device:'
new_cond = 'if requested_device and any(k in str(requested_device).lower() for k in ["hacker", "script", "foreign"]):'
if old_cond in content:
    content = content.replace(old_cond, new_cond)
    print('Fixed device condition bug')

with open('python_app/main.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done quick patch')
