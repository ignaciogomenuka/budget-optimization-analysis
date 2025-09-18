#!/usr/bin/env python3
"""
Enhanced Dataset Calculator
Adds calculated columns for ROAS, quartiles, marginal ROAS, efficiency drops, and saturation flags
"""

import pandas as pd
import numpy as np

def calculate_enhanced_metrics(df):
    """
    Add calculated columns to the dataset:
    1. ROAS = revenue / spend
    2. Quartile = spend quartiles within each client_id-platform combination
    3. Marginal_ROAS = average(revenue) / average(spend) within each quartile
    4. Efficiency_Drop = percentage change in Marginal_ROAS vs previous quartile
    5. Saturation_Flag = True if Efficiency_Drop < -15%
    """
    
    print("🚀 Starting enhanced metrics calculation...")
    
    # Create a copy to avoid modifying the original
    enhanced_df = df.copy()
    
    # 1. Calculate ROAS
    print("📊 Calculating ROAS...")
    enhanced_df['ROAS'] = np.where(
        enhanced_df['spend'] > 0,
        enhanced_df['revenue'] / enhanced_df['spend'],
        0
    )
    
    # Initialize new columns
    enhanced_df['Quartile'] = ''
    enhanced_df['Marginal_ROAS'] = 0.0
    enhanced_df['Efficiency_Drop'] = 0.0
    enhanced_df['Saturation_Flag'] = False
    
    print("📈 Processing quartiles and marginal ROAS by client-platform...")
    
    # Process each client-platform combination
    for client in enhanced_df['client_id'].unique():
        for platform in enhanced_df['platform'].unique():
            
            # Filter data for current client-platform
            mask = (enhanced_df['client_id'] == client) & (enhanced_df['platform'] == platform)
            client_platform_data = enhanced_df[mask].copy()
            
            if len(client_platform_data) == 0:
                continue
                
            print(f"   Processing {client} - {platform} ({len(client_platform_data)} records)")
            
            # 2. Create spend quartiles within this client-platform group
            try:
                client_platform_data['Quartile'] = pd.qcut(
                    client_platform_data['spend'], 
                    q=4, 
                    labels=['Q1', 'Q2', 'Q3', 'Q4'],
                    duplicates='drop'  # Handle cases where spend values are identical
                )
            except ValueError as e:
                # If qcut fails (e.g., too few unique values), use cut instead
                print(f"   Warning: Using cut instead of qcut for {client}-{platform}: {e}")
                client_platform_data['Quartile'] = pd.cut(
                    client_platform_data['spend'],
                    bins=4,
                    labels=['Q1', 'Q2', 'Q3', 'Q4']
                )
            
            # 3. Calculate Marginal ROAS for each quartile
            quartile_stats = client_platform_data.groupby('Quartile').agg({
                'spend': 'mean',
                'revenue': 'mean'
            }).reset_index()
            
            # Calculate marginal ROAS for each quartile
            quartile_stats['Marginal_ROAS'] = np.where(
                quartile_stats['spend'] > 0,
                quartile_stats['revenue'] / quartile_stats['spend'],
                0
            )
            
            # 4. Calculate Efficiency Drop (percentage change from previous quartile)
            quartile_stats['Efficiency_Drop'] = quartile_stats['Marginal_ROAS'].pct_change() * 100
            quartile_stats['Efficiency_Drop'] = quartile_stats['Efficiency_Drop'].fillna(0)
            
            # 5. Set Saturation Flag (True if Efficiency_Drop < -15%)
            quartile_stats['Saturation_Flag'] = quartile_stats['Efficiency_Drop'] < -15
            
            # Map the calculated values back to the original dataframe
            for _, quartile_row in quartile_stats.iterrows():
                quartile = quartile_row['Quartile']
                
                # Create mask for this specific quartile within client-platform
                quartile_mask = mask & (client_platform_data['Quartile'] == quartile).reindex(enhanced_df.index, fill_value=False)
                
                # Update the enhanced dataframe
                enhanced_df.loc[quartile_mask, 'Quartile'] = quartile
                enhanced_df.loc[quartile_mask, 'Marginal_ROAS'] = quartile_row['Marginal_ROAS']
                enhanced_df.loc[quartile_mask, 'Efficiency_Drop'] = quartile_row['Efficiency_Drop']
                enhanced_df.loc[quartile_mask, 'Saturation_Flag'] = quartile_row['Saturation_Flag']
    
    print("✅ Enhanced metrics calculation completed!")
    return enhanced_df

def generate_summary_report(df):
    """Generate a summary report of the enhanced dataset"""
    
    print("\n" + "="*60)
    print("📋 ENHANCED DATASET SUMMARY REPORT")
    print("="*60)
    
    print(f"\n📊 DATASET OVERVIEW:")
    print(f"   Total Records: {len(df):,}")
    print(f"   Date Range: {df['week'].min()} to {df['week'].max()}")
    print(f"   Clients: {', '.join(df['client_id'].unique())}")
    print(f"   Platforms: {', '.join(df['platform'].unique())}")
    
    print(f"\n💰 FINANCIAL METRICS:")
    print(f"   Total Spend: ${df['spend'].sum():,.2f}")
    print(f"   Total Revenue: ${df['revenue'].sum():,.2f}")
    print(f"   Overall ROAS: {df['revenue'].sum() / df['spend'].sum():.2f}x")
    
    print(f"\n📈 ROAS DISTRIBUTION:")
    roas_stats = df['ROAS'].describe()
    print(f"   Mean ROAS: {roas_stats['mean']:.2f}x")
    print(f"   Median ROAS: {roas_stats['50%']:.2f}x")
    print(f"   Min ROAS: {roas_stats['min']:.2f}x")
    print(f"   Max ROAS: {roas_stats['max']:.2f}x")
    
    print(f"\n🎯 QUARTILE DISTRIBUTION:")
    quartile_counts = df['Quartile'].value_counts().sort_index()
    for quartile, count in quartile_counts.items():
        pct = (count / len(df)) * 100
        print(f"   {quartile}: {count:,} records ({pct:.1f}%)")
    
    print(f"\n⚠️ SATURATION ANALYSIS:")
    saturation_count = df['Saturation_Flag'].sum()
    saturation_pct = (saturation_count / len(df)) * 100
    print(f"   Records with Saturation Flag: {saturation_count:,} ({saturation_pct:.1f}%)")
    
    # Client-Platform breakdown
    print(f"\n🏢 CLIENT-PLATFORM BREAKDOWN:")
    client_platform_summary = df.groupby(['client_id', 'platform']).agg({
        'spend': 'sum',
        'revenue': 'sum',
        'ROAS': 'mean',
        'Marginal_ROAS': 'mean',
        'Saturation_Flag': 'sum'
    }).round(2)
    
    client_platform_summary['Overall_ROAS'] = client_platform_summary['revenue'] / client_platform_summary['spend']
    client_platform_summary = client_platform_summary.round(2)
    
    print(client_platform_summary[['spend', 'revenue', 'Overall_ROAS', 'Marginal_ROAS', 'Saturation_Flag']])
    
    print(f"\n📊 TOP PERFORMING COMBINATIONS (by ROAS):")
    top_performers = df.groupby(['client_id', 'platform']).agg({
        'revenue': 'sum',
        'spend': 'sum'
    })
    top_performers['ROAS'] = top_performers['revenue'] / top_performers['spend']
    top_performers = top_performers.sort_values('ROAS', ascending=False)
    
    for i, (idx, row) in enumerate(top_performers.head().iterrows()):
        client, platform = idx
        print(f"   {i+1}. {client} - {platform}: {row['ROAS']:.2f}x ROAS")

def main():
    """Main execution function"""
    
    # Load the dataset
    try:
        print("📂 Loading dataset...")
        df = pd.read_csv('bi_case_study_campaigns_12m.csv')
        print(f"✅ Loaded {len(df):,} records from bi_case_study_campaigns_12m.csv")
    except FileNotFoundError:
        print("❌ Error: bi_case_study_campaigns_12m.csv not found!")
        print("   Make sure the file exists in the current directory.")
        return
    
    # Verify required columns exist
    required_columns = ['client_id', 'platform', 'week', 'spend', 'revenue']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"❌ Error: Missing required columns: {missing_columns}")
        print(f"   Available columns: {list(df.columns)}")
        return
    
    # Calculate enhanced metrics
    enhanced_df = calculate_enhanced_metrics(df)
    
    # Generate summary report
    generate_summary_report(enhanced_df)
    
    # Export enhanced dataset
    output_filename = 'bi_case_study_campaigns_enhanced.csv'
    print(f"\n💾 Exporting enhanced dataset to: {output_filename}")
    enhanced_df.to_csv(output_filename, index=False)
    
    # Verify export
    import os
    file_size = os.path.getsize(output_filename) / (1024 * 1024)  # Size in MB
    print(f"✅ Export completed!")
    print(f"📁 File: {output_filename}")
    print(f"📊 Size: {file_size:.2f} MB")
    print(f"🔢 Columns: {len(enhanced_df.columns)} (added 5 new columns)")
    
    # Show sample of enhanced data
    print(f"\n📋 SAMPLE OF ENHANCED DATASET:")
    sample_cols = ['client_id', 'platform', 'week', 'spend', 'revenue', 
                   'ROAS', 'Quartile', 'Marginal_ROAS', 'Efficiency_Drop', 'Saturation_Flag']
    print(enhanced_df[sample_cols].head(10).to_string(index=False))
    
    print(f"\n🎯 DATASET READY FOR ANALYSIS!")
    print(f"📈 Use the enhanced dataset for advanced budget optimization insights")

if __name__ == "__main__":
    main()