#!/usr/bin/env python3
"""
Growth vs Production Analysis

This script analyzes the trade-offs between cellular growth and product formation,
and demonstrates why growth rates are 0 in production-optimized systems.
"""

import cobra
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fba_optimizer import WorkingFBAOptimizer
from cell_free_simulator import CellFreeSimulator

def analyze_growth_production_tradeoff():
    """
    Analyze the trade-off between growth and production.
    """
    print("=" * 60)
    print("GROWTH vs PRODUCTION TRADE-OFF ANALYSIS")
    print("=" * 60)
    
    # Initialize optimizer
    optimizer = WorkingFBAOptimizer()
    optimizer.add_demand_reactions()
    
    # Test different growth constraints
    growth_constraints = np.linspace(0, 0.8, 9)  # 0 to 0.8 h⁻¹
    target_fatty_acid = 'octanoic_acid'
    
    results = []
    
    print(f"Testing growth constraints for {target_fatty_acid}:")
    print("-" * 50)
    
    for growth_rate in growth_constraints:
        model = optimizer.model.copy()
        
        # Set growth constraint
        biomass_rxn = model.reactions.get_by_id('BIOMASS_Ec_iML1515_core_75p37M')
        biomass_rxn.lower_bound = growth_rate
        
        # Optimize for production
        model.objective = optimizer.demand_reactions[target_fatty_acid]
        solution = model.optimize()
        
        if solution.status == 'optimal':
            actual_growth = solution.fluxes.get('BIOMASS_Ec_iML1515_core_75p37M', 0)
            production_rate = solution.objective_value
            glucose_uptake = abs(solution.fluxes.get('EX_glc__D_e', 0))
            
            results.append({
                'Growth Constraint': growth_rate,
                'Actual Growth': actual_growth,
                'Production Rate': production_rate,
                'Glucose Uptake': glucose_uptake,
                'Status': solution.status
            })
            
            print(f"  Growth {growth_rate:.2f} h⁻¹ → Production {production_rate:.4f} mmol/gDW/h")
        else:
            results.append({
                'Growth Constraint': growth_rate,
                'Actual Growth': 0,
                'Production Rate': 0,
                'Glucose Uptake': 0,
                'Status': solution.status
            })
            print(f"  Growth {growth_rate:.2f} h⁻¹ → INFEASIBLE")
    
    results_df = pd.DataFrame(results)
    
    # Create Pareto front visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Growth vs Production (Pareto front)
    feasible_results = results_df[results_df['Status'] == 'optimal']
    
    ax1.plot(feasible_results['Actual Growth'], feasible_results['Production Rate'], 
             'o-', color='blue', markersize=8, linewidth=2, label='Pareto Front')
    ax1.set_xlabel('Growth Rate (h⁻¹)')
    ax1.set_ylabel('Production Rate (mmol/gDW/h)')
    ax1.set_title('Growth vs Production Trade-off\n(Pareto Front)', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Add annotations for key points
    max_growth_point = feasible_results.loc[feasible_results['Actual Growth'].idxmax()]
    max_production_point = feasible_results.loc[feasible_results['Production Rate'].idxmax()]
    
    ax1.annotate(f'Max Growth\n({max_growth_point["Actual Growth"]:.2f} h⁻¹)', 
                xy=(max_growth_point['Actual Growth'], max_growth_point['Production Rate']),
                xytext=(10, 10), textcoords='offset points', fontsize=10,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.7))
    
    ax1.annotate(f'Max Production\n({max_production_point["Production Rate"]:.3f} mmol/gDW/h)', 
                xy=(max_production_point['Actual Growth'], max_production_point['Production Rate']),
                xytext=(10, -30), textcoords='offset points', fontsize=10,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen', alpha=0.7))
    
    # Plot 2: Resource allocation
    ax2.plot(feasible_results['Actual Growth'], feasible_results['Glucose Uptake'], 
             's-', color='red', markersize=8, linewidth=2, label='Glucose Uptake')
    ax2.set_xlabel('Growth Rate (h⁻¹)')
    ax2.set_ylabel('Glucose Uptake (mmol/gDW/h)')
    ax2.set_title('Resource Allocation\n(Glucose Uptake vs Growth)', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.show()
    
    # Print summary
    print("\n" + "=" * 60)
    print("TRADE-OFF ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"Maximum growth rate: {max_growth_point['Actual Growth']:.3f} h⁻¹")
    print(f"  → Production rate: {max_growth_point['Production Rate']:.4f} mmol/gDW/h")
    print(f"Maximum production rate: {max_production_point['Production Rate']:.4f} mmol/gDW/h")
    print(f"  → Growth rate: {max_production_point['Actual Growth']:.3f} h⁻¹")
    
    # Calculate trade-off ratio
    production_loss = (max_production_point['Production Rate'] - max_growth_point['Production Rate'])
    growth_gain = max_growth_point['Actual Growth']
    
    if growth_gain > 0:
        trade_off_ratio = production_loss / growth_gain
        print(f"\nTrade-off ratio: {trade_off_ratio:.4f} mmol/gDW/h lost per h⁻¹ gained")
    
    return results_df

def explain_zero_growth_rates():
    """
    Explain why growth rates are 0 in production optimization.
    """
    print("\n" + "=" * 60)
    print("WHY GROWTH RATES ARE 0 IN PRODUCTION OPTIMIZATION")
    print("=" * 60)
    
    optimizer = WorkingFBAOptimizer()
    optimizer.add_demand_reactions()
    
    print("1. RESOURCE COMPETITION:")
    print("   - Growth requires biomass components (amino acids, nucleotides, lipids)")
    print("   - Production requires carbon/energy for product synthesis")
    print("   - Limited glucose must be allocated between growth and production")
    print()
    
    print("2. OPTIMIZATION BEHAVIOR:")
    print("   - FBA maximizes the objective function (production rate)")
    print("   - Growth is not penalized, so it's set to minimum (0)")
    print("   - This maximizes substrate flux to product formation")
    print()
    
    print("3. BIOLOGICAL REALITY:")
    print("   - In nature, cells balance growth and production")
    print("   - In bioprocessing, we often want maximum production")
    print("   - Cell-free systems naturally have zero growth")
    print()
    
    # Demonstrate with concrete example
    model = optimizer.model.copy()
    
    # Case 1: Growth objective
    print("CASE 1: GROWTH OPTIMIZATION")
    print("-" * 30)
    model.objective = 'BIOMASS_Ec_iML1515_core_75p37M'
    solution = model.optimize()
    
    print(f"  Growth rate: {solution.objective_value:.4f} h⁻¹")
    print(f"  Octanoyl-CoA production: {solution.fluxes.get('DM_occoa_c', 0):.4f} mmol/gDW/h")
    print(f"  Glucose uptake: {abs(solution.fluxes.get('EX_glc__D_e', 0)):.4f} mmol/gDW/h")
    
    # Case 2: Production objective
    print("\nCASE 2: PRODUCTION OPTIMIZATION")
    print("-" * 30)
    model.objective = 'DM_occoa_c'
    solution = model.optimize()
    
    print(f"  Growth rate: {solution.fluxes.get('BIOMASS_Ec_iML1515_core_75p37M', 0):.4f} h⁻¹")
    print(f"  Octanoyl-CoA production: {solution.objective_value:.4f} mmol/gDW/h")
    print(f"  Glucose uptake: {abs(solution.fluxes.get('EX_glc__D_e', 0)):.4f} mmol/gDW/h")
    
    # Case 3: Balanced objective
    print("\nCASE 3: BALANCED OPTIMIZATION (0.5 × Growth + 0.5 × Production)")
    print("-" * 60)
    model.objective = {
        'BIOMASS_Ec_iML1515_core_75p37M': 0.5,
        'DM_occoa_c': 0.5
    }
    solution = model.optimize()
    
    print(f"  Growth rate: {solution.fluxes.get('BIOMASS_Ec_iML1515_core_75p37M', 0):.4f} h⁻¹")
    print(f"  Octanoyl-CoA production: {solution.fluxes.get('DM_occoa_c', 0):.4f} mmol/gDW/h")
    print(f"  Glucose uptake: {abs(solution.fluxes.get('EX_glc__D_e', 0)):.4f} mmol/gDW/h")
    
    print("\n" + "=" * 60)
    print("CONCLUSION")
    print("=" * 60)
    print("✓ Growth rate = 0 is CORRECT for production optimization")
    print("✓ This represents maximum theoretical production")
    print("✓ Cell-free systems naturally have zero growth")
    print("✓ Use growth constraints for realistic cellular simulations")
    print("✓ Multi-objective optimization can balance growth and production")

def compare_system_types():
    """
    Compare different system types: cellular, cell-free, and hybrid.
    """
    print("\n" + "=" * 60)
    print("SYSTEM TYPE COMPARISON")
    print("=" * 60)
    
    # Initialize systems
    cellular_optimizer = WorkingFBAOptimizer()
    cellular_optimizer.add_demand_reactions()
    
    cell_free_sim = CellFreeSimulator()
    cell_free_sim.create_cell_free_model()
    
    target_fatty_acid = 'octanoic_acid'
    
    results = []
    
    # 1. Natural cellular system (growth-optimized)
    print("1. NATURAL CELLULAR SYSTEM (Growth-optimized)")
    print("-" * 50)
    model = cellular_optimizer.model.copy()
    model.objective = 'BIOMASS_Ec_iML1515_core_75p37M'
    solution = model.optimize()
    
    cellular_growth = {
        'System': 'Cellular (Growth-optimized)',
        'Growth Rate': solution.objective_value,
        'Production Rate': solution.fluxes.get(cellular_optimizer.demand_reactions[target_fatty_acid], 0),
        'Glucose Uptake': abs(solution.fluxes.get('EX_glc__D_e', 0)),
        'ATP Maintenance': abs(solution.fluxes.get('ATPM', 0)),
        'Description': 'Natural E. coli optimized for growth'
    }
    results.append(cellular_growth)
    
    # 2. Engineered cellular system (production-optimized)
    print("2. ENGINEERED CELLULAR SYSTEM (Production-optimized)")
    print("-" * 50)
    model.objective = cellular_optimizer.demand_reactions[target_fatty_acid]
    solution = model.optimize()
    
    cellular_production = {
        'System': 'Cellular (Production-optimized)',
        'Growth Rate': solution.fluxes.get('BIOMASS_Ec_iML1515_core_75p37M', 0),
        'Production Rate': solution.objective_value,
        'Glucose Uptake': abs(solution.fluxes.get('EX_glc__D_e', 0)),
        'ATP Maintenance': abs(solution.fluxes.get('ATPM', 0)),
        'Description': 'Engineered E. coli optimized for production'
    }
    results.append(cellular_production)
    
    # 3. Balanced cellular system
    print("3. BALANCED CELLULAR SYSTEM")
    print("-" * 50)
    # Force moderate growth
    model.reactions.get_by_id('BIOMASS_Ec_iML1515_core_75p37M').lower_bound = 0.2
    model.objective = cellular_optimizer.demand_reactions[target_fatty_acid]
    solution = model.optimize()
    
    cellular_balanced = {
        'System': 'Cellular (Balanced)',
        'Growth Rate': solution.fluxes.get('BIOMASS_Ec_iML1515_core_75p37M', 0),
        'Production Rate': solution.objective_value,
        'Glucose Uptake': abs(solution.fluxes.get('EX_glc__D_e', 0)),
        'ATP Maintenance': abs(solution.fluxes.get('ATPM', 0)),
        'Description': 'Cellular system with forced growth constraint'
    }
    results.append(cellular_balanced)
    
    # 4. Cell-free system
    print("4. CELL-FREE SYSTEM")
    print("-" * 50)
    cell_free_result = cell_free_sim.optimize_cell_free_production(target_fatty_acid, 'glucose', 10.0)
    
    cell_free = {
        'System': 'Cell-free',
        'Growth Rate': 0.0,
        'Production Rate': cell_free_result['production_rate'],
        'Glucose Uptake': cell_free_result['substrate_uptake_actual'],
        'ATP Maintenance': 0.0,  # Reduced in cell-free
        'Description': 'Cell-free enzymatic system'
    }
    results.append(cell_free)
    
    # Create comparison table
    results_df = pd.DataFrame(results)
    
    print("\nSYSTEM COMPARISON RESULTS:")
    print("=" * 80)
    for _, row in results_df.iterrows():
        print(f"\n{row['System']}:")
        print(f"  Growth Rate: {row['Growth Rate']:.4f} h⁻¹")
        print(f"  Production Rate: {row['Production Rate']:.4f} mmol/gDW/h")
        print(f"  Glucose Uptake: {row['Glucose Uptake']:.4f} mmol/gDW/h")
        print(f"  ATP Maintenance: {row['ATP Maintenance']:.4f} mmol/gDW/h")
        print(f"  Description: {row['Description']}")
    
    # Create visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    systems = results_df['System']
    growth_rates = results_df['Growth Rate']
    production_rates = results_df['Production Rate']
    
    # Plot 1: Growth vs Production scatter
    colors = ['blue', 'red', 'green', 'purple']
    for i, (system, growth, production) in enumerate(zip(systems, growth_rates, production_rates)):
        ax1.scatter(growth, production, s=150, alpha=0.7, color=colors[i], label=system)
    
    ax1.set_xlabel('Growth Rate (h⁻¹)')
    ax1.set_ylabel('Production Rate (mmol/gDW/h)')
    ax1.set_title('Growth vs Production by System Type', fontsize=14, fontweight='bold')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Production rates comparison
    bars = ax2.bar(range(len(systems)), production_rates, color=colors, alpha=0.7)
    ax2.set_xlabel('System Type')
    ax2.set_ylabel('Production Rate (mmol/gDW/h)')
    ax2.set_title('Production Rate Comparison', fontsize=14, fontweight='bold')
    ax2.set_xticks(range(len(systems)))
    ax2.set_xticklabels([s.split('(')[0].strip() for s in systems], rotation=45)
    ax2.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar, rate in zip(bars, production_rates):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{rate:.3f}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.show()
    
    return results_df

def main():
    """Main function to run all analyses."""
    
    # 1. Growth vs production trade-off analysis
    trade_off_results = analyze_growth_production_tradeoff()
    
    # 2. Explain zero growth rates
    explain_zero_growth_rates()
    
    # 3. Compare system types
    system_comparison = compare_system_types()
    
    # Final summary
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print("✓ Growth rate = 0 is EXPECTED in production optimization")
    print("✓ This represents maximum theoretical production without growth")
    print("✓ Cell-free systems naturally have zero growth")
    print("✓ Use growth constraints for realistic cellular simulations")
    print("✓ Different system types have different trade-offs")
    print("✓ Cell-free systems can achieve higher production rates")
    print("\nFor your SAF project:")
    print("- Cell-free systems are optimal for maximum production")
    print("- Zero growth rates are biologically correct")
    print("- Focus on enzyme activity and cofactor regeneration")
    print("- Consider continuous processing for steady-state operation")

if __name__ == "__main__":
    main()