"""
Simple data processing script: No pandas/numpy dependency
"""
import os
import csv
import random

# Create processed directory
os.makedirs('data/processed', exist_ok=True)

print("="*60)
print("Generating Affordable Housing Data")
print("="*60)

# Set random seed
random.seed(42)

cities = ['New York, NY', 'Los Angeles, CA', 'Chicago, IL', 
          'Detroit, MI', 'Cleveland, OH', 'Philadelphia, PA',
          'San Francisco, CA', 'Boston, MA']

# 1. Create policy coverage data
print("\n1. Creating policy coverage data...")
severe_cost_burden_renters = {
    'New York, NY': 850,
    'Los Angeles, CA': 720,
    'Chicago, IL': 380,
    'Detroit, MI': 120,
    'Cleveland, OH': 85,
    'Philadelphia, PA': 220,
    'San Francisco, CA': 180,
    'Boston, MA': 150
}

policy_data = []
for city in cities:
    public_housing = random.randint(20, 150) * 1000
    vouchers = random.randint(50, 300) * 1000
    lihtc = random.randint(30, 200) * 1000
    section8 = random.randint(10, 80) * 1000
    
    total_subsidized = public_housing + vouchers + lihtc + section8
    cost_burden_renters = severe_cost_burden_renters.get(city, 100) * 1000
    coverage_ratio = (total_subsidized / cost_burden_renters * 100) if cost_burden_renters > 0 else 0
    
    policy_data.append({
        'city': city,
        'severe_cost_burden_renters': cost_burden_renters,
        'public_housing_units': public_housing,
        'voucher_households': vouchers,
        'lihtc_units': lihtc,
        'section8_units': section8,
        'total_subsidized': total_subsidized,
        'coverage_ratio': round(coverage_ratio, 2),
        'subsidized_per_100_burdened': round(coverage_ratio, 2)
    })

with open('data/processed/policy_coverage.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=policy_data[0].keys())
    writer.writeheader()
    writer.writerows(policy_data)
print(f"✓ Created policy coverage data for {len(policy_data)} cities")

# 2. Create policy mix data
print("\n2. Creating policy mix data...")
policy_mix_data = []
for city in cities:
    if city in ['New York, NY', 'San Francisco, CA', 'Boston, MA']:
        mix = {
            'city': city,
            'city_type': 'Strong Market',
            'public_housing_pct': 15,
            'voucher_pct': 25,
            'lihtc_pct': 45,
            'section8_pct': 10,
            'iz_pct': 5
        }
    elif city in ['Detroit, MI', 'Cleveland, OH']:
        mix = {
            'city': city,
            'city_type': 'Legacy City',
            'public_housing_pct': 40,
            'voucher_pct': 35,
            'lihtc_pct': 15,
            'section8_pct': 8,
            'iz_pct': 2
        }
    else:
        mix = {
            'city': city,
            'city_type': 'Mixed',
            'public_housing_pct': 25,
            'voucher_pct': 30,
            'lihtc_pct': 30,
            'section8_pct': 10,
            'iz_pct': 5
        }
    policy_mix_data.append(mix)

with open('data/processed/policy_mix.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=policy_mix_data[0].keys())
    writer.writeheader()
    writer.writerows(policy_mix_data)
print(f"✓ Created policy mix data")

# 3. Create future risk data
print("\n3. Creating future risk data...")
years = list(range(2025, 2046))
expiration_data = []

for city in cities:
    for year in years:
        if year < 2030:
            expiring = random.randint(500, 3000)
        elif year < 2035:
            expiring = random.randint(1000, 5000)
        else:
            expiring = random.randint(2000, 8000)
        
        expiration_data.append({
            'city': city,
            'year': year,
            'expiring_units': expiring,
            'policy_type': 'LIHTC' if random.random() > 0.3 else 'Section 8'
        })

with open('data/processed/expiring_units.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=expiration_data[0].keys())
    writer.writeheader()
    writer.writerows(expiration_data)
print(f"✓ Created future risk data ({len(expiration_data)} records)")

print("\n" + "="*60)
print("Data processing completed!")
print("="*60)

