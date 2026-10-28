with open('python_app/main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

repl_lines = [
    '            \ id\: a.id,\n',
    '            \shortAlertId\: \#ALT-\ + a.id[:8].upper(),\n',
    '            \transactionId\: a.transaction_id,\n',
    '            \shortTxId\: \#TX-\ + (a.transaction_id[:8].upper() if a.transaction_id else \N/A\),\n',
    '            \userId\: a.user_id,\n',
    '            \userName\: a.user.name if a.user else \Kh\xe1ch h\xe0ng\,\n',
    '            \userPhone\: (a.user.phone if a.user and a.user.phone else \0972445090\),\n',
    '            \riskScore\: a.risk_score,\n',
    '            \riskLevel\: a.risk_level,\n',
    '            \title\: a.title,\n',
    '            \description\: a.description,\n',
    '            \evidenceJson\: a.evidence_json,\n',
    '            \status\: a.status,\n',
    '            \createdAt\: a.created_at.isoformat(),\n',
    '            \user\: {\name\: a.user.name, \email\: a.user.email, \phone\: a.user.phone} if a.user else None,\n'
]

lines[661:672] = repl_lines

with open('python_app/main.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('REPLACED_SUCCESS')
