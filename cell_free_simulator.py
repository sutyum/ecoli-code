#!/usr/bin/env python3
"""
Cell-free system simulator using COBRA.

This module creates proper cell-free system simulations by removing growth
constraints and optimizing for production without cellular maintenance costs.
"""

import cobra
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Tuple
from cobra.core import Reaction, Metabolite
from fba_optimizer import WorkingFBAOptimizer

class CellFreeSimulator:
    """
    Simulator for cell-free enzymatic systems using COBRA.
    """
    
    def __init__(self, model_name: str = "iML1515"):
        """Initialize the cell-free simulator."""
        self.cellular_model = cobra.io.load_model(model_name)
        self.cell_free_model = None
        self.fatty_acid_map = {
            'butanoic_acid': 'btcoa_c',
            'hexanoic_acid': 'hxcoa_c', 
            'octanoic_acid': 'occoa_c',
            'decanoic_acid': 'dcacoa_c',
            'dodecanoic_acid': 'ddcacoa_c',
            'tetradecanoic_acid': 'tdcoa_c'
        }
        self.demand_reactions = {}
        
        print(f"Initialized cell-free simulator with {model_name}")
        
    def create_cell_free_model(self):
        """
        Create a cell-free model by removing growth constraints and 
        cellular maintenance reactions.
        """
        print("Creating cell-free model...")
        
        # Start with cellular model
        self.cell_free_model = self.cellular_model.copy()
        
        # Remove or constrain biomass reactions
        biomass_reactions = [rxn for rxn in self.cell_free_model.reactions 
                           if 'BIOMASS' in rxn.id or 'biomass' in rxn.name.lower()]
        
        print(f"Found {len(biomass_reactions)} biomass reactions:")
        for rxn in biomass_reactions:
            print(f"  {rxn.id}: {rxn.name}")
            # Set biomass to zero for cell-free system
            rxn.lower_bound = 0
            rxn.upper_bound = 0
            
        # Remove ATP maintenance (cell-free systems don't need cellular maintenance)
        maintenance_reactions = [rxn for rxn in self.cell_free_model.reactions 
                               if 'ATPM' in rxn.id or 'maintenance' in rxn.name.lower()]
        
        print(f"Found {len(maintenance_reactions)} maintenance reactions:")
        for rxn in maintenance_reactions:
            print(f"  {rxn.id}: {rxn.name}")
            # Reduce ATP maintenance for cell-free systems
            rxn.lower_bound = 0
            rxn.upper_bound = min(rxn.upper_bound, 1.0)  # Reduce maintenance
            
        # Add demand reactions for fatty acids
        self._add_demand_reactions()
        
        print("Cell-free model created successfully!")
        
    def _add_demand_reactions(self):
        """Add demand reactions for fatty acid CoA metabolites."""
        for name, met_id in self.fatty_acid_map.items():
            try:
                met = self.cell_free_model.metabolites.get_by_id(met_id)
                
                demand_id = f"DM_{met_id}"
                if demand_id not in self.cell_free_model.reactions:
                    demand_rxn = Reaction(demand_id)
                    demand_rxn.name = f"{name} demand (cell-free)"
                    demand_rxn.lower_bound = 0
                    demand_rxn.upper_bound = 1000
                    demand_rxn.add_metabolites({met: -1})
                    self.cell_free_model.add_reactions([demand_rxn])
                    
                    self.demand_reactions[name] = demand_id
                    print(f"  Added cell-free demand for {name}: {demand_id}")
                    
            except KeyError:
                print(f"  Warning: {met_id} not found for {name}")
    
    def optimize_cell_free_production(self, 
                                    fatty_acid_name: str,
                                    substrate: str = "glucose",
                                    substrate_uptake: float = 10.0) -> Dict:
        """
        Optimize fatty acid production in cell-free system.
        
        Args:
            fatty_acid_name: Name of fatty acid to optimize
            substrate: Primary substrate ("glucose", "formate", "acetate")
            substrate_uptake: Substrate uptake rate (mmol/gDW/h)
            
        Returns:
            optimization_results: Dictionary with results
        """
        if self.cell_free_model is None:
            self.create_cell_free_model()
            
        if fatty_acid_name not in self.fatty_acid_map:
            raise ValueError(f"Fatty acid '{fatty_acid_name}' not supported")
            
        # Create optimization model
        opt_model = self.cell_free_model.copy()
        
        # Set substrate medium
        if substrate == "glucose":
            opt_model.medium = {
                'EX_glc__D_e': substrate_uptake,
                'EX_o2_e': 20.0,  # Aerobic conditions
                'EX_pi_e': 1000.0,
                'EX_nh4_e': 1000.0,
                'EX_so4_e': 1000.0,
                'EX_mg2_e': 1000.0,
                'EX_k_e': 1000.0,
                'EX_fe2_e': 1000.0,
                'EX_ca2_e': 1000.0,
                'EX_mn2_e': 1000.0,
                'EX_zn2_e': 1000.0,
                'EX_cu2_e': 1000.0,
                'EX_cobalt2_e': 1000.0,
                'EX_mobd_e': 1000.0
            }
        elif substrate == "formate":
            opt_model.medium = {
                'EX_for_e': substrate_uptake,
                'EX_o2_e': 20.0,
                'EX_pi_e': 1000.0,
                'EX_nh4_e': 1000.0,
                'EX_so4_e': 1000.0,
                'EX_mg2_e': 1000.0,
                'EX_k_e': 1000.0,
                'EX_fe2_e': 1000.0,
                'EX_ca2_e': 1000.0,
                'EX_mn2_e': 1000.0,
                'EX_zn2_e': 1000.0,
                'EX_cu2_e': 1000.0,
                'EX_cobalt2_e': 1000.0,
                'EX_mobd_e': 1000.0
            }
        elif substrate == "acetate":
            opt_model.medium = {
                'EX_ac_e': substrate_uptake,
                'EX_o2_e': 20.0,
                'EX_pi_e': 1000.0,
                'EX_nh4_e': 1000.0,
                'EX_so4_e': 1000.0,
                'EX_mg2_e': 1000.0,
                'EX_k_e': 1000.0,
                'EX_fe2_e': 1000.0,
                'EX_ca2_e': 1000.0,
                'EX_mn2_e': 1000.0,
                'EX_zn2_e': 1000.0,
                'EX_cu2_e': 1000.0,
                'EX_cobalt2_e': 1000.0,
                'EX_mobd_e': 1000.0
            }
        
        # Set objective
        demand_id = self.demand_reactions[fatty_acid_name]
        opt_model.objective = demand_id
        
        # Optimize
        solution = opt_model.optimize()
        
        if solution.status == 'optimal':
            results = {
                'fatty_acid': fatty_acid_name,
                'substrate': substrate,
                'substrate_uptake': substrate_uptake,
                'production_rate': solution.objective_value,
                'status': solution.status,
                'growth_rate': 0.0,  # Cell-free systems don't grow
                'substrate_uptake_actual': abs(solution.fluxes.get(f'EX_{substrate[0:3]}_e', 0)),
                'atp_consumption': abs(solution.fluxes.get('ATPM', 0)),
                'solution': solution,
                'model': opt_model
            }
            
            # Calculate yield
            if results['substrate_uptake_actual'] > 0:
                results['yield_mol_per_mol_substrate'] = results['production_rate'] / results['substrate_uptake_actual']
            else:
                results['yield_mol_per_mol_substrate'] = 0
                
            # Calculate specific productivity (more relevant for cell-free)
            results['specific_productivity'] = results['production_rate']  # mmol/gDW/h
            
            print(f"Cell-free optimization successful for {fatty_acid_name}")
            print(f"  Substrate: {substrate}")
            print(f"  Production rate: {results['production_rate']:.4f} mmol/gDW/h")
            print(f"  Yield: {results['yield_mol_per_mol_substrate']:.4f} mol/mol {substrate}")
            
        else:
            results = {
                'fatty_acid': fatty_acid_name,
                'substrate': substrate,
                'production_rate': 0,
                'status': solution.status,
                'error': f"Optimization failed: {solution.status}"
            }
            print(f"Cell-free optimization failed for {fatty_acid_name}: {solution.status}")
        
        return results
    
    def compare_cellular_vs_cell_free(self, fatty_acid_name: str = "octanoic_acid") -> Dict:
        """
        Compare cellular vs cell-free production for the same fatty acid.
        
        Returns:
            comparison_results: Dictionary with cellular and cell-free results
        """
        print(f"Comparing cellular vs cell-free production for {fatty_acid_name}")
        print("=" * 60)
        
        # Cellular optimization (with growth)
        cellular_optimizer = WorkingFBAOptimizer()
        cellular_optimizer.add_demand_reactions()
        
        # Force some growth in cellular system
        cellular_model = cellular_optimizer.model.copy()
        cellular_model.reactions.get_by_id('BIOMASS_Ec_iML1515_core_75p37M').lower_bound = 0.1
        cellular_model.objective = cellular_optimizer.demand_reactions[fatty_acid_name]
        cellular_solution = cellular_model.optimize()
        
        cellular_results = {
            'production_rate': cellular_solution.objective_value,
            'growth_rate': cellular_solution.fluxes.get('BIOMASS_Ec_iML1515_core_75p37M', 0),
            'glucose_uptake': abs(cellular_solution.fluxes.get('EX_glc__D_e', 0)),
            'atp_maintenance': abs(cellular_solution.fluxes.get('ATPM', 0)),
            'system_type': 'cellular'
        }
        
        # Cell-free optimization (no growth)
        if self.cell_free_model is None:
            self.create_cell_free_model()
            
        cell_free_results = self.optimize_cell_free_production(fatty_acid_name, "glucose", 10.0)
        
        # Calculate improvements
        production_improvement = (cell_free_results['production_rate'] / 
                                cellular_results['production_rate']) if cellular_results['production_rate'] > 0 else 0
        
        comparison = {
            'fatty_acid': fatty_acid_name,
            'cellular': cellular_results,
            'cell_free': cell_free_results,
            'production_improvement': production_improvement,
            'advantages_cell_free': [
                'No growth constraint',
                'No ATP maintenance cost',
                'Higher substrate conversion efficiency',
                'No cellular byproducts'
            ]
        }
        
        print("\nCOMPARISON RESULTS:")
        print(f"  Cellular production:   {cellular_results['production_rate']:.4f} mmol/gDW/h")
        print(f"  Cell-free production:  {cell_free_results['production_rate']:.4f} mmol/gDW/h")
        print(f"  Improvement:           {production_improvement:.2f}x")
        print(f"  Cellular growth:       {cellular_results['growth_rate']:.4f} h⁻¹")
        print(f"  Cell-free growth:      {cell_free_results['growth_rate']:.4f} h⁻¹")
        
        return comparison
    
    def test_substrate_preferences(self, fatty_acid_name: str = "octanoic_acid") -> pd.DataFrame:
        """
        Test different substrates for cell-free production.
        
        Returns:
            substrate_results: DataFrame with results for different substrates
        """
        print(f"Testing substrate preferences for {fatty_acid_name}")
        print("=" * 50)
        
        substrates = {
            'glucose': 10.0,
            'formate': 20.0,  # Higher uptake rate for formate
            'acetate': 15.0
        }
        
        results = []
        
        for substrate, uptake_rate in substrates.items():
            try:
                result = self.optimize_cell_free_production(fatty_acid_name, substrate, uptake_rate)
                results.append({
                    'Substrate': substrate,
                    'Uptake Rate': uptake_rate,
                    'Production Rate (mmol/gDW/h)': result['production_rate'],
                    'Yield (mol/mol substrate)': result['yield_mol_per_mol_substrate'],
                    'Status': result['status']
                })
            except Exception as e:
                results.append({
                    'Substrate': substrate,
                    'Uptake Rate': uptake_rate,
                    'Production Rate (mmol/gDW/h)': 0,
                    'Yield (mol/mol substrate)': 0,
                    'Status': f'Error: {e}'
                })
        
        results_df = pd.DataFrame(results)
        print("\nSUBSTRATE PREFERENCE RESULTS:")
        print(results_df.to_string(index=False))
        
        return results_df
    
    def visualize_comparison(self, comparison_results: Dict):
        """Create visualization comparing cellular vs cell-free production."""
        
        # Extract data
        cellular_prod = comparison_results['cellular']['production_rate']
        cell_free_prod = comparison_results['cell_free']['production_rate']
        cellular_growth = comparison_results['cellular']['growth_rate']
        cell_free_growth = comparison_results['cell_free']['growth_rate']
        
        # Create visualization
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Production rates
        systems = ['Cellular', 'Cell-free']
        production_rates = [cellular_prod, cell_free_prod]
        
        bars1 = ax1.bar(systems, production_rates, color=['lightblue', 'lightgreen'], alpha=0.7)
        ax1.set_title('Production Rates Comparison', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Production Rate (mmol/gDW/h)')
        ax1.grid(True, alpha=0.3)
        
        # Add value labels
        for bar, rate in zip(bars1, production_rates):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{rate:.3f}', ha='center', va='bottom', fontsize=12)
        
        # Growth rates
        growth_rates = [cellular_growth, cell_free_growth]
        
        bars2 = ax2.bar(systems, growth_rates, color=['lightcoral', 'lightgray'], alpha=0.7)
        ax2.set_title('Growth Rates Comparison', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Growth Rate (h⁻¹)')
        ax2.grid(True, alpha=0.3)
        
        # Add value labels
        for bar, rate in zip(bars2, growth_rates):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{rate:.3f}', ha='center', va='bottom', fontsize=12)
        
        plt.tight_layout()
        plt.show()
        
        # Print advantages
        print("\nCELL-FREE SYSTEM ADVANTAGES:")
        for advantage in comparison_results['advantages_cell_free']:
            print(f"  ✓ {advantage}")

def main():
    """Demonstration of cell-free system simulation."""
    print("=" * 60)
    print("CELL-FREE SYSTEM SIMULATION DEMO")
    print("=" * 60)
    
    # Initialize simulator
    simulator = CellFreeSimulator()
    
    # Create cell-free model
    simulator.create_cell_free_model()
    
    # Test cell-free production
    print("\n1. CELL-FREE PRODUCTION OPTIMIZATION:")
    print("-" * 50)
    result = simulator.optimize_cell_free_production('octanoic_acid', 'glucose', 10.0)
    
    # Compare cellular vs cell-free
    print("\n2. CELLULAR vs CELL-FREE COMPARISON:")
    print("-" * 50)
    comparison = simulator.compare_cellular_vs_cell_free('octanoic_acid')
    
    # Test substrate preferences
    print("\n3. SUBSTRATE PREFERENCE TESTING:")
    print("-" * 50)
    substrate_results = simulator.test_substrate_preferences('octanoic_acid')
    
    # Visualize results
    print("\n4. VISUALIZATION:")
    print("-" * 50)
    simulator.visualize_comparison(comparison)
    
    print("\n" + "=" * 60)
    print("CELL-FREE SIMULATION COMPLETE!")
    print("=" * 60)
    
    # Key insights
    print("\nKEY INSIGHTS:")
    print("- Cell-free systems eliminate growth constraints")
    print("- No ATP maintenance costs in cell-free systems")
    print("- Higher substrate conversion efficiency")
    print("- Growth rate = 0 is expected and correct for cell-free")
    print("- Production rates can be higher without cellular overhead")

if __name__ == "__main__":
    main()