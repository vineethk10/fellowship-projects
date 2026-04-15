"""
Session 04 — Data Structures Deep Dive
Agentic AI Builders Fellowship · Phase 1: Python for AI
My domain: Job Application Tracker 

Logs company name, role, date applied, and status; shows pipeline summary 
and pending follow-ups. Covers dictionaries, status filtering, date handling, 
and formatted summary output.
"""


MAX_RECORDS = 50

records = [
    {
        'company': 'Google',
        'role': 'Software Engineer',
        'date_applied': '2025-01-15',
        'status': 'interview',
        'tags': ['FAANG', 'backend', 'competitive']
    },
    {
        'company': 'Microsoft',
        'role': 'Cloud Architect',
        'date_applied': '2025-01-20',
        'status': 'pending',
        'tags': ['FAANG', 'cloud', 'architecture']
    },
    {
        'company': 'OpenAI',
        'role': 'AI Research Scientist',
        'date_applied': '2025-01-10',
        'status': 'rejected',
        'tags': ['AI', 'research', 'competitive']
    },
    {
        'company': 'Anthropic',
        'role': 'ML Engineer',
        'date_applied': '2025-01-25',
        'status': 'interview',
        'tags': ['AI', 'machine-learning', 'research']
    },
]


def add_record(records_list, company, role, date_applied, status, **fields):
    if len(records_list) >= MAX_RECORDS:
        print(f'[LIMIT] List is full. Maximum: {MAX_RECORDS}.')
        return
    new_record = {
        'company': company,
        'role': role,
        'date_applied': date_applied,
        'status': status,
        **fields
    }
    records_list.append(new_record)
    print(f'[ADDED] {company} — {role} saved.')


def list_all_records(records_list):
    if not records_list:
        print('[EMPTY] No records yet.')
        return
    sorted_records = sorted(records_list, key=lambda r: r['company'])
    print(f'\n=== All Applications ({len(sorted_records)}) ===')
    for record in sorted_records:
        print(f" {record['company']} — {record['role']}")
        for key, value in record.items():
            if key not in ['company', 'role']:
                print(f'  {key}: {value}')


def search_records(records_list, search_term):
    """Return a list of records whose company or role contains the search term."""
    results = [
        record for record in records_list
        if search_term.lower() in record['company'].lower() 
        or search_term.lower() in record['role'].lower()
    ]
    return results


def display_tags(records_list):
    """Return a set of every unique tag used across all records."""
    all_tags = set()
    for record in records_list:
        for tag in record.get('tags', []):
            all_tags.add(tag)
    return all_tags


def filter_by_status(records_list, status):
    """Return all records with a specific status."""
    results = [
        record for record in records_list
        if record.get('status', '').lower() == status.lower()
    ]
    return results


def main():
    """Run a demo of the full data model."""
    print(f'=== {__file__} — Session 04 Demo ===\n')
    
    list_all_records(records)
    
    print('\n--- Adding a new record ---')
    add_record(
        records, 
        'Tesla', 
        'AI/ML Engineer',
        '2025-02-01',
        'pending',
        tags=['AI', 'autonomous-vehicles', 'hardware']
    )
    
    print('\n--- Searching for "Engineer" ---')
    results = search_records(records, 'Engineer')
    for r in results:
        print(f" Found: {r['company']} — {r['role']}")
    
    print('\n--- All applications in interview stage ---')
    interview_records = filter_by_status(records, 'interview')
    for r in interview_records:
        print(f" {r['company']} — {r['role']} (applied: {r['date_applied']})")
    
    print('\n--- All unique tags ---')
    unique_tags = display_tags(records)
    print(f' Tags: {sorted(unique_tags)}')


if __name__ == '__main__':
    main()
