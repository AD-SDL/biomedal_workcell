from opentrons import protocol_api
import itertools
from opentrons.protocol_api import SINGLE


metadata = {
    'protocolName': 'Protein Design fdglu',
    'author': 'LDRD team ',
    'description': 'fdglu assay preparation',
    'source': 'FlexAS/pd_fdglu_assay_81.py'
}

requirements = {"robotType": "Flex", "apiLevel": "2.20"}

# Protocol Configuration
config = {
    # PCR product settings
    'combinations': [[18,10,2],[11,19,3],[4,20,12],[21,13,5]], # 1-indexed source well numbers (kept for total calculation)
    'fdglu_volume': 100,    # µL of PCR product to transfer to reaction plate
    'source_samples_volume': 20,
    'protein_and_buffer_volume': 20,
    'internal_standards_wells': [1, 2, 3, 4, 5], # 1-indexed well positions (A1, B1, C1, D1, E!) in the internal standards column [copied in this order leaving empty wells for later controls in the assay protocol]
    'protein_and_buffer_wells': [15, 16],
    'fdglu_col': 5,

    # Incubation settings
    'heater_shaker_temp': 37,     # °C for heater/shaker
    'pause_duration': 5,          # minutes for pause after reaction assembly (PF400 to sealer and back)
    'shaking_duration': 180,      # minutes (3 hours) for shaking (CFPS)
    'shaking_speed': 200,         # rpm for shaking (Is this optimal for CFPS? The pilots CFPS were run without shaking without issues in the assays) #TODO 100 is too low 200-3000

    # Reagent mixing settings (using 8-channel pipette)
    # Right now we assume that the combined reagents fit into one well (max 150µL). Using 25 uL reactions this is sufficient for 6 reactions (6 columns).
    # The number of columns is calculated based on the total number of combinations + 1 for internal standards (for this eample 3 columns are needed)
    'reagent_mix_A_column': 5,    # Column number for mix A (1-indexed)
    'reagent_mix_B_column': 7,    # Column number for mix B (1-indexed)
    'reagent_mixing_column': 8,   # Column number for mixing reagents (1-indexed)
    'reagent_mix_A_volume': 60,  # µL from mix A column to mixing column
    'reagent_mix_B_volume': 30,   # µL from mix B column to mixing column
    'final_reagent_volume': 23,   # µL from mixing column to template columns
    'mixing_repetitions': 5,      # Number of mix cycles
    'mixing_volume': 20,          # Volume for mixing (appropriate for ~25µL total)

    # Template column settings
    # This is coming from the PCR dilution/assay protocol
    'template_columns': [7, 8],  # List of column numbers with templates (1-indexed)

    # Temperature settings
    'temperature': 4,  # °C

    # Labware
    'controls_plate_type': 'nest_96_wellplate_100ul_pcr_full_skirt',  # Diluted PCR products
    'cfps_plate_type': 'nest_96_wellplate_100ul_pcr_full_skirt', # Reagent plate for reactions
    'fdglu_plate_type': 'corning_96_wellplate_360ul_flat', # Internal standards
    'pcr_adapter_type': 'opentrons_96_pcr_adapter',  # Aluminum adapter for PCR plates
    'tip_rack_type_50_01': 'opentrons_flex_96_filtertiprack_50ul',
    'tip_rack_type_50_02': 'opentrons_flex_96_filtertiprack_50ul',
    # 'tip_rack_type_50_03': 'opentrons_flex_96_tiprack_50ul',
    'pipette_type_50': 'flex_8channel_50',
    'reagent_plate_type': 'nest_12_reservoir_15ml',


    # Deck positions
    'temp_module_01_position': 'B1',
    'temp_module_02_position': 'C1',         # Temperature module for reaction assembly
    'shaker_module_position': 'D1',        # Heater/shaker module for incubation
    'controls_plate_position': 'B2',         # Diluted PCR products plate
    'reagent_plate_position': 'A1',   # Final position for internal standards
    'cfps_plate_position': 'C2', # Initial staging position for reaction plate
    'fdglu_plate_position': 'D2',
    'tip_rack_position_50_01': 'A2',
    'tip_rack_position_50_02': 'A3',
    # 'tip_rack_position_50_03': 'B3',
}


def calculate_total_combinations(combinations):
    """Calculate total number of combinations without generating them"""
    total = 1
    for sublist in combinations:
        total *= len(sublist)
    return total


def generate_all_combinations(combinations):
    """Generate all possible combinations from the jagged array"""
    return list(itertools.product(*combinations))


def calculate_internal_standards_column(config):
    """
    Calculate which column to use for internal standards based on total combinations

    Args:
        config: Configuration dictionary

    Returns:
        int: 1-indexed column number for internal standards
    """
    total_combinations = calculate_total_combinations(config['combinations'])

    # Calculate how many full columns are needed for PCR products (8 wells per column)
    columns_needed = (total_combinations + 7) // 8  # Ceiling division

    # Internal standards go in the next available column
    internal_standards_column = columns_needed + 1

    return internal_standards_column, total_combinations



def remove_rmf(protocol, cfps_plate, reagent_plate, pipette, config):
    # remove 23 ul from wells f12, g12, h12
    wells_to_remove = [93, 94, 95]
    dest_well = reagent_plate.wells()[11] # last col of reagent plate
    for well in wells_to_remove:
        source_well = cfps_plate.wells()[well]
        pipette.transfer(
        27.6,
        source_well,
        dest_well,
        new_tip='always',  # Use fresh tip for each transfer
        )

def fdglu_to_plate(protocol, reagent_plate, fdglu_plate, pipette, config): #TODO make sure this is all wells in plate
    # 100 ul of assay into all wells
    combinations = config['combinations']
    num_samples = calculate_total_combinations(combinations)
    fdglu_volume = 33.3
    columns_needed = (num_samples + 7) // 8
    source_well = reagent_plate.columns()[5]
    pipette.pick_up_tip()
    for i in range(12):
        dest_well = fdglu_plate.columns()[i]
        pipette.transfer(
        fdglu_volume,
        source_well,
        dest_well,
        new_tip='never',
        )

        pipette.transfer(
        fdglu_volume,
        source_well,
        dest_well,
        new_tip='never',
        )

        pipette.transfer(
        fdglu_volume,
        source_well,
        dest_well,
        new_tip='never',
        )
    pipette.drop_tip()

def cfps_to_dest(protocol, cfps_plate, fdglu_plate, pipette, config):
    cfps_volume = 20
    for i in range(12):
        dest_well = fdglu_plate.columns()[i]
        source_well = cfps_plate.columns()[i]
        pipette.transfer(
        cfps_volume,
        source_well,
        dest_well,
        new_tip='always',
        mix_after = (3, 30)
        )

def controls_to_dest(protocol, controls_plate, fdglu_plate, pipette, config):
   #controls in f3, g3, h3 into fdglu f12, g12, h12
   controls = [21, 22, 23]
   dest = [93, 94, 95]
   for i in range(3):
       source_well = controls_plate.wells()[controls[i]]
       dest_well = fdglu_plate.wells()[dest[i]]
       pipette.transfer(
        20,
        source_well,
        dest_well,
        new_tip='always',
        mix_after = (3, 30)
        )













def run(protocol):
    # Load temperature module and adapter for reaction assembly
    temp_mod1 = protocol.load_module(module_name="temperature module gen2", location=config['temp_module_01_position'])
    temp_adapter1 = temp_mod1.load_adapter(config['pcr_adapter_type'])

    temp_mod2 = protocol.load_module(module_name="temperature module gen2", location=config['temp_module_02_position'])
    temp_adapter2 = temp_mod2.load_adapter(config['pcr_adapter_type'])

    # Load heater/shaker module for incubation
    shaker_mod = protocol.load_module(module_name="heaterShakerModuleV1", location=config['shaker_module_position'])
    shaker_adapter = shaker_mod.load_adapter(config['pcr_adapter_type'])

    # Set temperature for reaction assembly
    # temp_mod.set_temperature(config['temperature'])

    # Load source plate with diluted PCR products on B2
    controls_plate = protocol.load_labware(config['controls_plate_type'], config['controls_plate_position'])
    controls_plate.set_offset(x=0.4, y=0.4, z=0.0)

    # Load internal standards plate initially on B4, then move to B3
    cfps_plate = protocol.load_labware(config['cfps_plate_type'], config['cfps_plate_position'])
    cfps_plate.set_offset(x=0.4, y=0.4, z=0.0)

    fdglu_plate = protocol.load_labware(config['fdglu_plate_type'], config['fdglu_plate_position'])
    fdglu_plate.set_offset(x=0.4, y=0.4, z=0.0)

    reagent_plate = protocol.load_labware(config['reagent_plate_type'], config['reagent_plate_position'])

    # Load tip racks

    tiprack_50_1 = protocol.load_labware(
        load_name=config['tip_rack_type_50_01'], location=config['tip_rack_position_50_01']
    )
    tiprack_50_2 = protocol.load_labware(
        load_name=config['tip_rack_type_50_02'], location=config['tip_rack_position_50_02']
    )
    # tiprack_50_3 = protocol.load_labware(
    #     load_name=config['tip_rack_type_50_03'], location=config['tip_rack_position_50_03']
    # )


    # Pipettes
    p50 = protocol.load_instrument('flex_8channel_50', mount='right', tip_racks=[tiprack_50_1, tiprack_50_2])
    p50s = protocol.load_instrument('flex_1channel_50', mount='left', tip_racks=[tiprack_50_1, tiprack_50_2])

    p50.configure_nozzle_layout(style='COLUMN', start='A1', tip_racks=[tiprack_50_1, tiprack_50_2])
    # p50s.configure_nozzle_layout(style=SINGLE, start='A1', tip_racks=[tiprack_200])


    chute = protocol.load_waste_chute()

    remove_rmf(protocol=protocol,
               cfps_plate=cfps_plate,
               reagent_plate=reagent_plate,
               pipette=p50s,
               config = config)

    fdglu_to_plate(protocol=protocol,
                   reagent_plate=reagent_plate,
                   fdglu_plate=fdglu_plate,
                   pipette=p50,
                   config=config)

    cfps_to_dest(protocol=protocol,
                 cfps_plate=cfps_plate,
                 fdglu_plate=fdglu_plate,
                 pipette=p50,
                 config=config)

    controls_to_dest(protocol=protocol,
                     controls_plate=controls_plate,
                     fdglu_plate=fdglu_plate,
                     pipette=p50s,
                     config=config)