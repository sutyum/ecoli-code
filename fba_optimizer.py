"""
Working FBA Optimizer for Acetyl-CoA to Fatty Acids

This module provides a functional system for optimizing fatty acid production
using existing pathways in the E. coli model.
"""

import cobra
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from cobra.core import Reaction, Metabolite
from cobra.flux_analysis import flux_variability_analysis
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkingFBAOptimizer:
    """
    Working FBA optimizer that uses existing fatty acid CoA metabolites.
    """
    
    def __init__(self, model_name: str = "iML1515"):
        """Initialize the FBA optimizer with E. coli model."""
        self.model = cobra.io.load_model(model_name)
        self.original_model = self.model.copy()
        
        # Map of common fatty acids to existing CoA metabolites
        self.fatty_acid_map = {
            'butanoic_acid': 'btcoa_c',      # Butanoyl-CoA
            'hexanoic_acid': 'hxcoa_c',      # Hexanoyl-CoA  
            'octanoic_acid': 'occoa_c',      # Octanoyl-CoA
            'decanoic_acid': 'dcacoa_c',     # Decanoyl-CoA
            'dodecanoic_acid': 'ddcacoa_c',  # Dodecanoyl-CoA
            'tetradecanoic_acid': 'tdcoa_c', # Tetradecanoyl-CoA
        }
        
        # Store demand reactions
        self.demand_reactions = {}
        
        logger.info(f"Loaded model: {model_name}")
        logger.info(f"Reactions: {len(self.model.reactions)}, Metabolites: {len(self.model.metabolites)}")
        
        # Check existing fatty acid CoA metabolites
        self._check_existing_fatty_acids()
    
    def _check_existing_fatty_acids(self):
        """Check which fatty acid CoA metabolites exist in the model."""
        logger.info("Checking existing fatty acid CoA metabolites...")
        for name, met_id in self.fatty_acid_map.items():
            try:
                met = self.model.metabolites.get_by_id(met_id)
                logger.info(f"  {name}: {met.name} ({met_id})")
            except KeyError:
                logger.warning(f"  {name}: {met_id} not found in model")
    
    def add_demand_reactions(self):
        """Add demand reactions for all fatty acid CoA metabolites."""
        logger.info("Adding demand reactions for fatty acid CoA metabolites...")
        
        for name, met_id in self.fatty_acid_map.items():
            try:
                met = self.model.metabolites.get_by_id(met_id)
                
                # Create demand reaction
                demand_id = f"DM_{met_id}"
                if demand_id not in self.model.reactions:
                    demand_rxn = Reaction(demand_id)
                    demand_rxn.name = f"{name} demand"
                    demand_rxn.lower_bound = 0
                    demand_rxn.upper_bound = 1000
                    demand_rxn.add_metabolites({met: -1})
                    self.model.add_reactions([demand_rxn])
                    
                    self.demand_reactions[name] = demand_id
                    logger.info(f"  Added demand for {name}: {demand_id}")
                else:
                    self.demand_reactions[name] = demand_id
                    logger.info(f"  Demand already exists for {name}: {demand_id}")
                    
            except KeyError:
                logger.warning(f"  Could not add demand for {name}: {met_id} not found")
    
    def optimize_fatty_acid_production(self, 
                                     fatty_acid_name: str,
                                     medium: Optional[Dict[str, float]] = None,
                                     knockouts: Optional[List[str]] = None) -> Dict:
        """
        Optimize production of a specific fatty acid.
        
        Args:
            fatty_acid_name: Name of fatty acid (e.g., 'octanoic_acid')
            medium: Custom medium composition
            knockouts: List of reaction IDs to knock out
            
        Returns:
            optimization_results: Dictionary with optimization results
        """
        if fatty_acid_name not in self.fatty_acid_map:
            raise ValueError(f"Fatty acid '{fatty_acid_name}' not supported. "
                           f"Available: {list(self.fatty_acid_map.keys())}")
        
        # Create model copy for optimization
        opt_model = self.model.copy()
        
        # Set medium
        if medium:
            opt_model.medium = medium
        else:
            # Default minimal medium with glucose
            opt_model.medium = {
                'EX_glc__D_e': 10.0,
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
        
        # Apply knockouts
        if knockouts:
            for ko in knockouts:
                try:
                    opt_model.reactions.get_by_id(ko).knock_out()
                    logger.info(f"Knocked out: {ko}")
                except KeyError:
                    logger.warning(f"Reaction {ko} not found for knockout")
        
        # Set objective to the demand reaction
        demand_id = self.demand_reactions[fatty_acid_name]
        opt_model.objective = demand_id
        
        # Optimize
        solution = opt_model.optimize()
        
        if solution.status == 'optimal':
            results = {
                'fatty_acid': fatty_acid_name,
                'production_rate': solution.objective_value,
                'status': solution.status,
                'growth_rate': solution.fluxes.get('BIOMASS_Ec_iML1515_core_75p37M', 0),
                'glucose_uptake': abs(solution.fluxes.get('EX_glc__D_e', 0)),
                'oxygen_uptake': abs(solution.fluxes.get('EX_o2_e', 0)),
                'solution': solution,
                'model': opt_model
            }
            
            # Calculate yield
            if results['glucose_uptake'] > 0:
                results['yield_mol_per_mol_glucose'] = results['production_rate'] / results['glucose_uptake']
            else:
                results['yield_mol_per_mol_glucose'] = 0
                
            logger.info(f"Optimization successful for {fatty_acid_name}")
            logger.info(f"Production rate: {results['production_rate']:.4f} mmol/gDW/h")
            
        else:
            results = {
                'fatty_acid': fatty_acid_name,
                'production_rate': 0,
                'status': solution.status,
                'error': f"Optimization failed: {solution.status}"
            }
            logger.error(f"Optimization failed for {fatty_acid_name}: {solution.status}")
        
        return results
    
    def optimize_all_fatty_acids(self, 
                                medium: Optional[Dict[str, float]] = None) -> Dict[str, Dict]:
        """
        Optimize production for all available fatty acids.
        
        Returns:
            results: Dictionary with results for each fatty acid
        """
        logger.info("Optimizing production for all fatty acids...")
        
        results = {}
        for fatty_acid_name in self.fatty_acid_map.keys():
            result = self.optimize_fatty_acid_production(fatty_acid_name, medium)
            results[fatty_acid_name] = result
            
        return results
    
    def screen_knockouts(self, 
                        fatty_acid_name: str,
                        knockout_candidates: List[str]) -> pd.DataFrame:
        """
        Screen knockout combinations for improved fatty acid production.
        
        Args:
            fatty_acid_name: Target fatty acid name
            knockout_candidates: List of reaction IDs to test
            
        Returns:
            results_df: DataFrame with knockout screening results
        """
        logger.info(f"Screening knockouts for {fatty_acid_name}...")
        
        results = []
        
        # Test baseline (no knockouts)
        baseline = self.optimize_fatty_acid_production(fatty_acid_name)
        results.append({
            'knockouts': 'none',
            'production_rate': baseline['production_rate'],
            'growth_rate': baseline['growth_rate'],
            'improvement': 0.0
        })
        
        # Test individual knockouts
        for ko in knockout_candidates:
            try:
                result = self.optimize_fatty_acid_production(fatty_acid_name, knockouts=[ko])
                improvement = ((result['production_rate'] - baseline['production_rate']) / 
                              baseline['production_rate'] * 100) if baseline['production_rate'] > 0 else 0
                
                results.append({
                    'knockouts': ko,
                    'production_rate': result['production_rate'],
                    'growth_rate': result['growth_rate'],
                    'improvement': improvement
                })
                
            except Exception as e:
                logger.warning(f"Knockout screening failed for {ko}: {e}")
        
        return pd.DataFrame(results).sort_values('improvement', ascending=False)
    
    def analyze_pathway_usage(self, fatty_acid_name: str) -> Dict:
        """
        Analyze which pathways are used for fatty acid production.
        
        Args:
            fatty_acid_name: Target fatty acid name
            
        Returns:
            pathway_analysis: Dictionary with pathway flux analysis
        """
        result = self.optimize_fatty_acid_production(fatty_acid_name)
        
        if result['status'] != 'optimal':
            return {'error': 'No optimal solution available'}
        
        solution = result['solution']
        
        # Find active reactions (flux > 0.001)
        active_reactions = {}
        for rxn_id, flux in solution.fluxes.items():
            if abs(flux) > 0.001:
                rxn = self.model.reactions.get_by_id(rxn_id)
                active_reactions[rxn_id] = {
                    'flux': flux,
                    'name': rxn.name,
                    'reaction': str(rxn.reaction)
                }
        
        # Find reactions involving the target fatty acid CoA
        target_met_id = self.fatty_acid_map[fatty_acid_name]
        target_met = self.model.metabolites.get_by_id(target_met_id)
        
        target_reactions = {}
        for rxn in target_met.reactions:
            if rxn.id in active_reactions:
                target_reactions[rxn.id] = active_reactions[rxn.id]
        
        return {
            'total_active_reactions': len(active_reactions),
            'target_fatty_acid_reactions': target_reactions,
            'production_rate': result['production_rate'],
            'key_pathways': self._identify_key_pathways(active_reactions)
        }
    
    def _identify_key_pathways(self, active_reactions: Dict) -> List[str]:
        """Identify key metabolic pathways being used."""
        pathways = []
        
        pathway_keywords = {
            'Glycolysis': ['PGI', 'PFK', 'FBA', 'TPI', 'GAPD', 'PGK', 'PGM', 'ENO', 'PYK'],
            'TCA Cycle': ['CS', 'ACONTa', 'ACONTb', 'ICDHyr', 'AKGDH', 'SUCOAS', 'SUCDi', 'FUM', 'MDH'],
            'Fatty Acid Synthesis': ['FACOAL', 'ACCOAL', 'FASYN'],
            'Acetyl-CoA': ['PDH', 'PTA', 'ACK', 'ACCOAL']
        }
        
        for pathway_name, keywords in pathway_keywords.items():
            if any(any(keyword in rxn_id for keyword in keywords) for rxn_id in active_reactions):
                pathways.append(pathway_name)
        
        return pathways
    
    def export_results(self, results: Dict[str, Dict], filename: str = "fatty_acid_optimization_results.xlsx"):
        """Export optimization results to Excel file."""
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Summary sheet
            summary_data = []
            for fatty_acid, result in results.items():
                if 'production_rate' in result:
                    summary_data.append({
                        'Fatty Acid': fatty_acid,
                        'Production Rate (mmol/gDW/h)': result['production_rate'],
                        'Growth Rate (h-1)': result.get('growth_rate', 0),
                        'Glucose Uptake (mmol/gDW/h)': result.get('glucose_uptake', 0),
                        'Yield (mol/mol glucose)': result.get('yield_mol_per_mol_glucose', 0),
                        'Status': result['status']
                    })
            
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Pathway analysis for each fatty acid
            for fatty_acid in results.keys():
                try:
                    pathway_data = self.analyze_pathway_usage(fatty_acid)
                    if 'error' not in pathway_data:
                        pathway_df = pd.DataFrame([
                            {'Metric': 'Production Rate', 'Value': pathway_data['production_rate']},
                            {'Metric': 'Total Active Reactions', 'Value': pathway_data['total_active_reactions']},
                            {'Metric': 'Key Pathways', 'Value': ', '.join(pathway_data['key_pathways'])}
                        ])
                        pathway_df.to_excel(writer, sheet_name=f'{fatty_acid}_pathway', index=False)
                except Exception as e:
                    logger.warning(f"Could not analyze pathway for {fatty_acid}: {e}")
        
        logger.info(f"Results exported to {filename}")
    
    def reset_model(self):
        """Reset model to original state."""
        self.model = self.original_model.copy()
        self.demand_reactions = {}
        logger.info("Model reset to original state")

def main():
    """Main function to demonstrate the working FBA optimizer."""
    print("=" * 60)
    print("WORKING FBA OPTIMIZER DEMONSTRATION")
    print("=" * 60)
    
    # Initialize optimizer
    optimizer = WorkingFBAOptimizer()
    
    # Add demand reactions
    optimizer.add_demand_reactions()
    
    # Test optimization for all fatty acids
    print("\n1. OPTIMIZING ALL FATTY ACIDS:")
    print("-" * 40)
    
    results = optimizer.optimize_all_fatty_acids()
    
    # Display results
    for fatty_acid, result in results.items():
        status = result['status']
        rate = result['production_rate']
        print(f"  {fatty_acid}: {rate:.4f} mmol/gDW/h ({status})")
    
    # Find best performing fatty acid
    best_fatty_acid = max(results.keys(), key=lambda x: results[x]['production_rate'])
    best_rate = results[best_fatty_acid]['production_rate']
    
    print(f"\n2. BEST PERFORMING FATTY ACID: {best_fatty_acid}")
    print(f"   Production rate: {best_rate:.4f} mmol/gDW/h")
    
    # Test knockout screening
    print("\n3. KNOCKOUT SCREENING:")
    print("-" * 40)
    
    knockout_candidates = ['ACALD', 'PTAr', 'ACKr', 'LDH_D', 'PFL']
    knockout_results = optimizer.screen_knockouts(best_fatty_acid, knockout_candidates)
    
    print("Top 5 knockout results:")
    for _, row in knockout_results.head(5).iterrows():
        improvement = row['improvement']
        symbol = "✓" if improvement > 0 else "✗"
        print(f"  {symbol} {row['knockouts']}: {improvement:+.1f}% improvement")
        print(f"     Production: {row['production_rate']:.4f} mmol/gDW/h")
    
    # Analyze pathway usage
    print("\n4. PATHWAY ANALYSIS:")
    print("-" * 40)
    
    pathway_analysis = optimizer.analyze_pathway_usage(best_fatty_acid)
    if 'error' not in pathway_analysis:
        print(f"  Active reactions: {pathway_analysis['total_active_reactions']}")
        print(f"  Key pathways: {', '.join(pathway_analysis['key_pathways'])}")
        print(f"  Target reactions: {len(pathway_analysis['target_fatty_acid_reactions'])}")
    
    # Export results
    print("\n5. EXPORTING RESULTS:")
    print("-" * 40)
    optimizer.export_results(results, "working_fba_results.xlsx")
    print("  Results exported to: working_fba_results.xlsx")
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    main()