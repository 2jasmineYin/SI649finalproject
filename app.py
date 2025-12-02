"""
Streamlit App: Affordable Housing Policy Tools Analysis
"""
import streamlit as st
import pandas as pd
import json
import os

# Page configuration
st.set_page_config(
    page_title="Affordable Housing Policy Tools Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("Bridging the Gap: Are Affordable Housing Policies Reaching Those Who Need Them Most?")
st.markdown("---")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["Overview", "The Crisis: Where Housing Affordability Hurts Most", "The Policy Response: Tools and Coverage", "Conclusions"]
)

# Load data
@st.cache_data
def load_data():
    """Load data"""
    try:
        with open('data/processed/policy_coverage.json', 'r') as f:
            policy_coverage = json.load(f)
        with open('data/processed/policy_mix.json', 'r') as f:
            policy_mix = json.load(f)
        with open('data/processed/expiring_units.json', 'r') as f:
            expiring_units = json.load(f)
        return policy_coverage, policy_mix, expiring_units
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None

policy_coverage, policy_mix, expiring_units = load_data()

if policy_coverage is None:
    st.stop()

# ============================================================================
# PARTNER'S SECTION: The Crisis: Where Housing Affordability Hurts Most
# ============================================================================
if page == "The Crisis: Where Housing Affordability Hurts Most":
    st.header("Part 1: The Crisis: Where Housing Affordability Hurts Most")
    
    st.markdown("""
    This section examines where housing affordability pressures are most severe, based on the ICMA article: 
    "The United States Housing Affordability Crisis: No Easy Solutions"
    """)
    
    # Subsection selector
    subsection = st.radio(
        "Select Analysis",
        ["1.1 Systemic vs. Strong-Market Cost Burden", "1.2 Cost Burden Across Income Groups", "1.3 COVID-19 Impact"],
        horizontal=True
    )
    
    st.markdown("---")
    
    # Subsection 1.1: Systemic vs. Strong-Market Cost Burden
    if subsection == "1.1 Systemic vs. Strong-Market Cost Burden":
        st.subheader("1.1 Systemic vs. Strong-Market Cost Burden")
        
        st.markdown("""
        Affordability crisis does not look the same everywhere. In some communities, even very low rents makes it difficult for low-wage workers. In others, rising prices are pushing cost burdens higher. Following Alan Mallach's ICMA framework, we distinguish between two overlapping and distinct patterns: **systemic cost burden** and **strong-market cost burden**.
        """)
        
        st.markdown("""
        **Systemic cost burden** describes places where very low-income households face high housing cost burdens even in markets that are not considered to be popular. By contrast, **strong-market cost burden** arises in high-demand metropolitan areas where incomes are higher on average but housing costs have risen even faster.
        """)
        
        # Visualization 1: Geographic Distribution
        st.subheader("Geographic Distribution of Cost Burden")
        
        try:
            with open('visualizations/burden_geographic_distribution.html', 'r', encoding='utf-8') as f:
                st.components.v1.html(f.read(), height=500)
        except FileNotFoundError:
            st.error("Visualization file not found: visualizations/burden_geographic_distribution.html")
        
        st.caption("""
        **Figure 1:** Number of severely cost-burdened renter households (spending more than 50 percent of income on rent) in each of the eight study cities, colored by city type (strong-market, legacy, or mixed). Strong-market metros combine large numbers of severely burdened renters with intense price pressures, while legacy cities have smaller populations but still carry a high absolute burden relative to their size. *Data Source: Analysis of policy coverage data.*
        """)
    
    # Subsection 1.2: Cost Burden Across Income Groups
    elif subsection == "1.2 Cost Burden Across Income Groups":
        st.subheader("1.2 Cost Burden Across Income Groups")
        
        st.markdown("""
        Another way to view the crisis is to step back from individual cities and compare **types** of markets. When we group our eight metros into strong-market, legacy, and mixed-market categories, we can see both how much of the country's severe cost burden each type carries and how much subsidy coverage it has relative to that burden.
        """)
        
        # Visualization 2: Income Groups
        st.subheader("Burden and Subsidy Coverage by City Type")
        
        try:
            with open('visualizations/burden_by_income_group.html', 'r', encoding='utf-8') as f:
                st.components.v1.html(f.read(), height=500)
        except FileNotFoundError:
            st.error("Visualization file not found: visualizations/burden_by_income_group.html")
        
        st.caption("""
        **Figure 2:** Interactive scatterplot showing the relationship between need and coverage by city type. Each point represents a city type (strong-market, legacy, mixed); its position on the x-axis shows the share of all severely cost-burdened renters in our eight-city sample, while its position on the y-axis shows subsidized units per 100 severely burdened renters. Point size reflects the total number of severely burdened renters. Dashed reference lines mark the overall average burden share and average coverage level, making it easy to see which city types carry a disproportionate share of need and which fall below average on subsidy coverage.
        """)
    
    # Subsection 1.3: COVID-19 Impact
    elif subsection == "1.3 COVID-19 Impact":
        st.subheader("1.3 COVID-19 Impact on Housing Affordability")
        
        st.markdown("""
        The COVID-19 pandemic didn't start the affordability crisis but it makes it more serious. The FHFA House Price Index and Zillow's typical home value going upward throughout the 2010s. After 2020, the dots representing each year jump to much higher levels.
        """)
        
        # Visualization 3: COVID Trends
        st.subheader("National Housing Costs Before and After COVID-19")
        
        try:
            with open('visualizations/covid_trends.html', 'r', encoding='utf-8') as f:
                st.components.v1.html(f.read(), height=500)
        except FileNotFoundError:
            st.error("Visualization file not found: visualizations/covid_trends.html")
        
        st.caption("""
        **Figure 3:** Interactive scatterplot of national housing costs from 2010 onward, combining the FHFA House Price Index with Zillow's typical U.S. home value. Each point represents a year; users can hover to see exact values and brush to zoom into specific time periods. The cluster of pre-2020 points contrasts with the higher, post-2020 cluster, highlighting how quickly housing costs escalated after the onset of COVID-19. *Data sources: FHFA HPI (seasonally adjusted) and Zillow ZHVI.*
        """)
    
        st.info("""
        **Key Finding:** COVID-19 magnified both *systemic* and *strong-market* cost burdens. Legacy and weaker-market cities saw affordability erode as national prices rose from unusually low baselines, while high-cost metros experienced some of the largest jumps in housing values. The result is a post-pandemic landscape in which renters at all income levels—especially the lowest-income households—face deeper and more widespread affordability pressures than in the previous decade.
    """)
    

# Overview page
elif page == "Overview":
    st.header("Project Overview")
    
    st.markdown("""
    ### Research Background
    
    In the United States, millions of families face severe housing cost burdens—spending more than half their income on rent. 
    Federal, state, and local policies attempt to provide relief, but are these policy tools actually reaching the communities 
    and households that need them most?
    
    ### Research Questions
    
    This project analyzes housing affordability from multiple angles:
    
    **Part 1: The Crisis** (Partner: Merrila Liu)
    - Where are housing affordability pressures most severe?
    - How does cost burden vary by income group and geography?
    - How did COVID-19 impact the crisis?
    
    **Part 2: The Policy Response** (Jing Yin)
    1. **Coverage Gap Analysis**: Are subsidized housing programs truly covering the "most burdened" areas?
    2. **Policy Mix Comparison**: Do different types of cities rely on different policy tool combinations?
    3. **Future Risk Analysis**: Are we "quietly losing" existing affordable units?
    
    ### Data Sources
    
    - HUD (U.S. Department of Housing and Urban Development) data
    - U.S. Census Bureau data
    - Local housing authority data
    - Penn IUR Policy Brief analysis
    """)
    
    # Display data summary
    st.subheader("Data Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Cities Analyzed", len(policy_coverage))
    
    with col2:
        total_burdened = sum(d['severe_cost_burden_renters'] for d in policy_coverage)
        st.metric("Total Severely Burdened Renters", f"{total_burdened/1000:.0f}K")
    
    with col3:
        total_subsidized = sum(d['total_subsidized'] for d in policy_coverage)
        st.metric("Total Subsidized Units", f"{total_subsidized/1000:.0f}K")

# ============================================================================
# YOUR SECTION: The Policy Response: Tools and Coverage
# ============================================================================
elif page == "The Policy Response: Tools and Coverage":
    st.header("Part 2: The Policy Response: Tools and Coverage")
    
    st.markdown("""
    This section analyzes whether affordable housing policy tools are effectively reaching the communities 
    that need them most, based on the Penn IUR Policy Brief.
    """)
    
    # Subsection selector
    subsection = st.radio(
        "Select Analysis",
        ["2.1 Coverage Gap Analysis", "2.2 Policy Mix Comparison", "2.3 Future Risk Analysis"],
        horizontal=True
    )
    
    st.markdown("---")
    
    # Subsection 2.1: Coverage Gap Analysis
    if subsection == "2.1 Coverage Gap Analysis":
        st.subheader("2.1 Coverage Gap Analysis")
        st.markdown("**Research Question:** Are subsidized housing programs truly covering the 'most burdened' areas?")
        
        st.markdown("""
        This analysis examines whether affordable housing programs are geographically aligned with communities experiencing 
        the most severe cost burdens.
        
        **Key Metrics**:
        - Number of severely cost-burdened renters (demand)
        - Total subsidized housing units (supply)
        - Coverage ratio: subsidized units per 100 severely burdened renters
        """)
        
        # Create dataframe
        df_coverage = pd.DataFrame(policy_coverage)
        
        # Visualization options
        viz_type = st.radio("Select Visualization Type", ["Demand vs Supply Comparison", "Coverage Ratio Analysis"], horizontal=True)
        
        if viz_type == "Demand vs Supply Comparison":
            st.subheader("Demand vs Supply Comparison")
            
            # Prepare data
            comparison_data = []
            for row in policy_coverage:
                comparison_data.append({
                    'city': row['city'],
                    'type': 'Severely Cost-Burdened Renters (Demand)',
                    'count': row['severe_cost_burden_renters']
                })
                comparison_data.append({
                    'city': row['city'],
                    'type': 'Subsidized Housing Units (Supply)',
                    'count': row['total_subsidized']
                })
            
            df_compare = pd.DataFrame(comparison_data)
            
            # Chart
            st.bar_chart(
                df_compare.pivot(index='city', columns='type', values='count'),
                height=400
            )
            
            st.caption("Note: Using logarithmic scale to better compare cities of different sizes")
        
        else:
            st.subheader("Coverage Ratio Analysis")
            
            # Sort
            df_coverage_sorted = df_coverage.sort_values('subsidized_per_100_burdened', ascending=False)
            
            # Bar chart
            st.bar_chart(
                df_coverage_sorted.set_index('city')['subsidized_per_100_burdened'],
                height=400
            )
            
            st.caption("Subsidized units per 100 severely burdened renters. Values below 100 indicate insufficient supply.")
        
        # Data table
        st.subheader("Detailed Data")
        st.dataframe(
            df_coverage[['city', 'severe_cost_burden_renters', 'total_subsidized', 
                         'subsidized_per_100_burdened']].style.format({
                'severe_cost_burden_renters': '{:,.0f}',
                'total_subsidized': '{:,.0f}',
                'subsidized_per_100_burdened': '{:.1f}'
            }),
            use_container_width=True
        )
        
        # Key findings
        st.info("""
        **Key Finding**:
        - Cities with the highest numbers of severely burdened renters often have the lowest ratios of subsidized units to need
        - This suggests policy tools are not effectively targeting communities experiencing the most severe burden challenges
        """)
    
    # Subsection 2.2: Policy Mix Comparison
    elif subsection == "2.2 Policy Mix Comparison":
        st.subheader("2.2 Policy Mix Comparison")
        st.markdown("**Research Question:** Do different types of cities rely on different policy tool combinations?")
        
        st.markdown("""
        This analysis explores whether different types of cities employ different combinations of policy tools.
        
        **Policy Tool Types**:
        - Public Housing
        - Housing Choice Vouchers
        - LIHTC (Low-Income Housing Tax Credit)
        - Section 8 Project-Based
        - Inclusionary Zoning
        """)
        
        # Create dataframe
        df_mix = pd.DataFrame(policy_mix)
        
        # Select cities
        selected_cities = st.multiselect(
            "Select Cities to Compare",
            df_mix['city'].tolist(),
            default=df_mix['city'].tolist()
        )
        
        if selected_cities:
            df_selected = df_mix[df_mix['city'].isin(selected_cities)]
            
            # Prepare stacked bar chart data
            mix_data = []
            for _, row in df_selected.iterrows():
                for policy in ['public_housing_pct', 'voucher_pct', 'lihtc_pct', 'section8_pct', 'iz_pct']:
                    policy_name = {
                        'public_housing_pct': 'Public Housing',
                        'voucher_pct': 'Housing Vouchers',
                        'lihtc_pct': 'LIHTC',
                        'section8_pct': 'Section 8',
                        'iz_pct': 'Inclusionary Zoning'
                    }[policy]
                    mix_data.append({
                        'city': row['city'],
                        'city_type': row['city_type'],
                        'policy': policy_name,
                        'percentage': row[policy]
                    })
            
            df_mix_long = pd.DataFrame(mix_data)
            
            # Stacked bar chart
            st.subheader("Policy Tool Mix (Percentage)")
            pivot_data = df_mix_long.pivot(index='city', columns='policy', values='percentage')
            st.bar_chart(pivot_data, height=400)
            
            # Grouped by city type
            st.subheader("Grouped by City Type")
            city_type_counts = df_selected['city_type'].value_counts()
            st.bar_chart(city_type_counts)
            
            # Data table
            st.subheader("Detailed Data")
            st.dataframe(
                df_selected[['city', 'city_type', 'public_housing_pct', 'voucher_pct', 
                             'lihtc_pct', 'section8_pct', 'iz_pct']].style.format({
                    'public_housing_pct': '{:.1f}%',
                    'voucher_pct': '{:.1f}%',
                    'lihtc_pct': '{:.1f}%',
                    'section8_pct': '{:.1f}%',
                    'iz_pct': '{:.1f}%'
                }),
                use_container_width=True
            )
        
        # Key findings
        st.info("""
        **Key Finding**:
        - **Strong-market cities** (e.g., New York, San Francisco) rely more on LIHTC and inclusionary zoning
        - **Legacy cities** (e.g., Detroit, Cleveland) rely more on public housing and vouchers
        - These differences reflect different market conditions and policy histories across cities
        """)
    
    # Subsection 2.3: Future Risk Analysis
    elif subsection == "2.3 Future Risk Analysis":
        st.subheader("2.3 Future Risk Analysis")
        st.markdown("**Research Question:** Are we 'quietly losing' existing affordable units?")
        
        st.markdown("""
        This analysis addresses a critical but often overlooked challenge: the expiration of affordability restrictions.
        
        **Risk Factors**:
        - LIHTC units typically have 15-year affordability requirements
        - Section 8 contracts also have expiration dates
        - After expiration, owners can convert units to market rate
        """)
        
        # Create dataframe
        df_expiring = pd.DataFrame(expiring_units)
        
        # Year range selection
        year_range = st.slider(
            "Select Year Range",
            min_value=int(df_expiring['year'].min()),
            max_value=int(df_expiring['year'].max()),
            value=(int(df_expiring['year'].min()), int(df_expiring['year'].max())),
            step=1
        )
        
        df_filtered = df_expiring[
            (df_expiring['year'] >= year_range[0]) & 
            (df_expiring['year'] <= year_range[1])
        ]
        
        # Aggregate by city and year
        df_summary = df_filtered.groupby(['city', 'year']).agg({
            'expiring_units': 'sum'
        }).reset_index()
        
        # Time series chart
        st.subheader("Expiring Units Time Series")
        
        # Select cities
        cities_to_show = st.multiselect(
            "Select Cities to Display",
            df_summary['city'].unique().tolist(),
            default=df_summary['city'].unique().tolist()[:5]
        )
        
        if cities_to_show:
            df_chart = df_summary[df_summary['city'].isin(cities_to_show)]
            pivot_chart = df_chart.pivot(index='year', columns='city', values='expiring_units')
            st.line_chart(pivot_chart, height=400)
        
        # Cumulative risk
        st.subheader("Cumulative Expiring Units")
        df_cumulative = df_summary.copy()
        df_cumulative = df_cumulative.sort_values(['city', 'year'])
        df_cumulative['cumulative'] = df_cumulative.groupby('city')['expiring_units'].cumsum()
        
        if cities_to_show:
            df_cumulative_filtered = df_cumulative[df_cumulative['city'].isin(cities_to_show)]
            pivot_cumulative = df_cumulative_filtered.pivot(index='year', columns='city', values='cumulative')
            st.area_chart(pivot_cumulative, height=400)
        
        # Data table
        st.subheader("Detailed Data")
        st.dataframe(
            df_summary.style.format({
                'expiring_units': '{:,.0f}'
            }),
            use_container_width=True
        )
        
        # Key findings
        st.warning("""
        **Key Finding**:
        - The number of expiring units increases significantly over the next 20 years
        - Cities with the highest numbers of expiring units often also have the highest numbers of severely burdened renters
        - This creates a "double burden" where communities already facing burden challenges must also cope with the risk of losing existing affordable units
        """)

# Conclusions
elif page == "Conclusions":
    st.header("Conclusions and Policy Recommendations")
    
    st.markdown("""
    ### Key Findings
    
    These three analyses reveal several critical insights:
    
    #### 1. Geographic Targeting Matters
    
    The data suggests that simply increasing the total number of affordable units is insufficient. Policy tools need to be 
    strategically deployed in communities with the highest need.
    
    **Recommendations**:
    - Reform LIHTC allocation to prioritize high-need areas
    - Expand voucher programs in markets with high cost burdens
    - Develop stronger inclusionary zoning requirements in strong-market cities
    
    #### 2. One Size Doesn't Fit All
    
    The different policy mixes across city types suggest that effective affordable housing policy must be tailored to local 
    market conditions.
    
    **Recommendations**:
    - Develop customized policies for different market types
    - Support local innovation and experimentation
    - Share best practices and lessons learned
    
    #### 3. Preservation Is as Important as Production
    
    The expiration timeline shows that preserving existing affordable units is as critical as creating new ones.
    
    **Recommendations**:
    - Expand Tenant Protection Voucher programs
    - Provide incentives for owners to renew affordability restrictions
    - Develop preservation funds to purchase at-risk properties
    
    ### System Needs Alignment
    
    The analysis reveals a fundamental misalignment: communities experiencing the most severe housing burden challenges are 
    not always the ones receiving the most support from policy tools.
    
    This misalignment occurs at multiple levels:
    - **Geographic**: High-need communities don't always receive proportional resources
    - **Tool Selection**: Different cities use different policy mixes, but these mixes aren't always optimized for local needs
    - **Temporal**: The risk of losing affordable units through expiring restrictions threatens progress
    
    ### Next Steps
    
    To address the affordable housing crisis, we need to:
    1. Better align policy tools with need
    2. Preserve existing affordable units
    3. Tailor policy approaches to local market conditions
    
    By doing so, we can begin to bridge the gap between the communities that need affordable housing most and the resources 
    available to help them.
    """)
    
    # Data sources
    st.markdown("---")
    st.caption("""
    **Data Sources**: HUD, U.S. Census Bureau, Local Housing Authorities
    
    **More Information**: Penn IUR Policy Brief: "An Overview of Affordable Housing in the United States"
    """)

# Footer
st.markdown("---")
st.caption("SI649 Narrative Visualization Project | December 2024")
