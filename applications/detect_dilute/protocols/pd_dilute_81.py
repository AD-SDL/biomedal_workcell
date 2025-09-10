from opentrons import protocol_api
import itertools
from opentrons.protocol_api import SINGLE


metadata = {
    'protocolName': 'Protein Design Dilute 81',
    'author': 'LDRD team ',
    'description': 'Dilution and Detection step for Protein Design',
    'source': 'FlexAS/pd_dilute_81.py'
}

requirements = {"robotType": "Flex", "apiLevel": "2.20"}


# Protocol Configuration
config = {
    # Reagent mixing
    'number_of_pcr_samples': 6,
    'sybrgreen_volume': 198,
    'pcr_sample_volume': 2,
    'water_volume': 18,
    'combinations': [[2,10,18],[3,11,19],[4,12,20],[5,13,21]],
    "num_controls": 5,

    # Master mix and reagent settings
    'pcr_master_mix_well_volume': 100,
    'pcr_master_mix_volume': 24,
    'water_well': 1,
    'master_mix_start_well': 48,
    'sybrgreen_well': 3,
    'columns_to_move_for_dilute': 6,
    'control_volume': 20,
    'pcr_plate_control_column': 1,


    # Temperature settings
    'temperature': 4,  # °C

    # Labware
    # 'source_plate_type': 'nest_96_wellplate_100ul_pcr_full_skirt',
    'diluted_pcr_plate_type': 'nest_96_wellplate_100ul_pcr_full_skirt',
    'pcr_plate_type': 'nest_96_wellplate_100ul_pcr_full_skirt',
    'controls_plate_type': 'nest_96_wellplate_100ul_pcr_full_skirt',
    # 'gg_plate_type': 'nest_96_wellplate_100ul_pcr_full_skirt',
    'reagent_plate_type': 'nest_12_reservoir_15ml',
    'sybrgreen_plate_type': 'corning_96_wellplate_360ul_flat',
    'tip_rack_type_50_01': 'opentrons_flex_96_tiprack_50ul',
    'tip_rack_type_50_02': 'opentrons_flex_96_tiprack_50ul',
    'tip_rack_type_50_03': 'opentrons_flex_96_tiprack_50ul',
    'pipette_type_50': 'flex_8channel_50',
    'tip_rack_type_200_01': 'opentrons_flex_96_tiprack_200ul',
    # 'pipette_type_1000': 'flex_8channel_1000',
    'controls_plate_type': 'nest_96_wellplate_100ul_pcr_full_skirt',

    # Deck positions
    'temp_module_01_position': 'B1',
    'temp_module_02_position': 'C1',
    # 'source_plate_initial_position': 'C1',
    # 'gg_plate_position': 'B2',
    'diluted_pcr_plate_position': 'C1',
    'pcr_plate_position': 'B2',
    'tip_rack_position_50_01': 'A2',
    'tip_rack_position_50_02': 'A3',
    'tip_rack_position_50_03': 'B3',
    'reagent_plate_position': 'A1',
    'sybrgreen_plate_position': 'C2',
    'controls_plate_position': 'B1'
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


def sybrgreen_to_dest(protocol, reagent_plate, sybrgreen_plate, pipette, config):
    sybrgreen_volume = config['sybrgreen_volume'] / 4
    # num_samples = config["number_of_pcr_samples"]
    combinations = config['combinations']
    num_samples = calculate_total_combinations(combinations)
    columns_needed = (num_samples + 7) // 8 
    columns_needed = columns_needed+1
    sybrgreen_well = reagent_plate.wells()[config['sybrgreen_well'] - 1]
    pipette.pick_up_tip()
    # first 50
    for col_idx in range(columns_needed):
        dest_well = sybrgreen_plate.columns()[col_idx]
        protocol.comment(f"\nTransferring to destination well {dest_well}:")
        pipette.transfer(
            sybrgreen_volume,
            sybrgreen_well,
            dest_well,
            new_tip='never',  # Use fresh tip for each transfer
        )
    # 100
    for col_idx in range(columns_needed):
        dest_well = sybrgreen_plate.columns()[col_idx]
        protocol.comment(f"\nTransferring to destination well {dest_well}:")
        pipette.transfer(
            sybrgreen_volume,
            sybrgreen_well,
            dest_well,
            new_tip='never',  # Use fresh tip for each transfer
        )
    # change well!
    sybrgreen_well = reagent_plate.wells()[config['sybrgreen_well']]
    # 150
    for col_idx in range(columns_needed):
        dest_well = sybrgreen_plate.columns()[col_idx]
        protocol.comment(f"\nTransferring to destination well {dest_well}:")
        pipette.transfer(
            sybrgreen_volume,
            sybrgreen_well,
            dest_well,
            new_tip='never',  # Use fresh tip for each transfer
        )
    #200
    for col_idx in range(columns_needed):
        dest_well = sybrgreen_plate.columns()[col_idx]
        protocol.comment(f"\nTransferring to destination well {dest_well}:")
        pipette.transfer(
            sybrgreen_volume,
            sybrgreen_well,
            dest_well,
            new_tip='never',  # Use fresh tip for each transfer
        )
    pipette.drop_tip()





def pcr_to_dest(protocol, pcr_plate, sybrgreen_plate, pipette, config):
    pcr_sample_volume = config['pcr_sample_volume']
    # num_samples = config["number_of_pcr_samples"]
    combinations = config['combinations']
    num_samples = calculate_total_combinations(combinations)
    columns_needed = (num_samples + 7) // 8

    for col_idx in range(columns_needed+1):
        source_well = pcr_plate.columns()[col_idx]
        dest_well = sybrgreen_plate.columns()[col_idx]
        protocol.comment(f"\nTransferring to destination well {dest_well}:")
        pipette.transfer(
            pcr_sample_volume,
            source_well,
            dest_well,
            new_tip='always',  # Use fresh tip for each transfer
            mix_after = (3, 20)
        )

def controls_to_sybrgreen(protocol, controls_plate, sybrgreen_plate, pipette, config):
    pcr_sample_volume = config['pcr_sample_volume']
    source_well = controls_plate.columns()[4]
    dest_well = sybrgreen_plate.columns()[11]
    pipette.transfer(
        pcr_sample_volume,
        source_well,
        dest_well,
        new_tip='always',  # Use fresh tip for each transfer
        mix_after = (3, 20)
    )

def water_to_pcr_dilution_wells(protocol, diluted_pcr, reagent_plate, pipette, config):
    water_volume = config['water_volume']
    combinations = config['combinations']
    num_samples = calculate_total_combinations(combinations)
    columns_needed = (num_samples + 7) // 8 
    columns_to_move = config['columns_to_move_for_dilute']
    water_well = config['water_well']
    source_well = reagent_plate.wells()[water_well - 1]
    pipette.pick_up_tip()
    for col_idx in range(columns_needed):
        dest_well = diluted_pcr.columns()[col_idx]
        protocol.comment(f"\nTransferring to destination well {dest_well}:")
        pipette.transfer(
            water_volume,
            source_well,
            dest_well,
            new_tip='never',  # Use fresh tip for each transfer
            # mix_after = (3, 20)
        )
    pipette.drop_tip()



def pcr_to_water(protocol, pcr_plate, diluted_pcr, pipette, config):
    pcr_sample_volume = config['pcr_sample_volume']
    combinations = config['combinations']
    num_samples = calculate_total_combinations(combinations)
    columns_needed = (num_samples + 7) // 8 
    columns_to_move = config['columns_to_move_for_dilute']

    for col_idx in range(columns_needed):
        dest_well = diluted_pcr.columns()[col_idx]
        source_well = pcr_plate.columns()[col_idx]
        protocol.comment(f"\nTransferring to destination well {dest_well}:")
        pipette.transfer(
            pcr_sample_volume,
            source_well,
            dest_well,
            new_tip='always',  # Use fresh tip for each transfer
            mix_after = (3, 20)
        )


def controls_to_pcr(protocol, diluted_pcr, controls_plate, pipette, config):
    control_volume = config['control_volume']
    num_controls = config['num_controls']
    control_column = config['pcr_plate_control_column']

    starting_dest_well = 88 # last col #TODO hardcoded

    for well in range(1, num_controls + 1):
        source_well = controls_plate.wells()[well-1]
        dest_well = diluted_pcr.wells()[starting_dest_well]
        pipette.transfer(
            control_volume,
            source_well,
            dest_well,
            new_tip='always',  # Use fresh tip for each transfer
        )  
        starting_dest_well+=1


def run(protocol: protocol_api.ProtocolContext):
    # Load temperature module and adapter
    temp_mod1 = protocol.load_module(module_name="temperature module gen2", location=config['temp_module_01_position'])
    temp_adapter1 = temp_mod1.load_adapter("opentrons_96_well_aluminum_block")

    temp_mod2 = protocol.load_module(module_name="temperature module gen2", location=config['temp_module_02_position'])
    temp_adapter2 = temp_mod2.load_adapter("opentrons_96_well_aluminum_block")

    # Set temperature
    temp_mod1.set_temperature(config['temperature']) #TODO: make seperate, or just set earlier, only 1 hour with plate
    temp_mod2.set_temperature(config['temperature']) #TODO: make seperate, or just set earlier, only 1 hour with plate

    # Load source plate initially on A4
    # source_plate = protocol.load_labware(config['source_plate_type'], config['source_plate_initial_position'])
    # source_plate = temp_adapter.load_labware(config['source_plate_type'])


    chute = protocol.load_waste_chute()

    # source_plate.set_offset(x=0.40, y=0.50, z=2.40)


    # Load destination plate
    pcr_plate = protocol.load_labware(config['pcr_plate_type'], config['pcr_plate_position'])
    pcr_plate.set_offset(x=0.4, y=0.4, z=0.0)

    diluted_pcr_plate = temp_adapter2.load_labware(config['diluted_pcr_plate_type'])
    # diluted_pcr_plate = protocol.load_labware(config['diluted_pcr_plate_type'], config['diluted_pcr_plate_position'])
    diluted_pcr_plate.set_offset(x=0.40, y=0.50, z=2.40)
    # gg_plate = protocol.load_labware(config['gg_plate_type'], config['gg_plate_position'])
    # gg_plate.set_offset(x=0.4, y=0.4, z=0.0)

    sybrgreen_plate = protocol.load_labware(config['sybrgreen_plate_type'], config['sybrgreen_plate_position'])

    reagent_plate = protocol.load_labware(config['reagent_plate_type'], config['reagent_plate_position'])

    controls_plate = temp_adapter1.load_labware(config['controls_plate_type'])
    # controls_plate = protocol.load_labware(config['controls_plate_type'], config['controls_plate_position'])
    controls_plate.set_offset(x=0.40, y=0.50, z=2.40)

    tiprack_50_1 = protocol.load_labware(
        load_name=config['tip_rack_type_50_01'], location=config['tip_rack_position_50_01']
    )
    tiprack_50_2 = protocol.load_labware(
        load_name=config['tip_rack_type_50_02'], location=config['tip_rack_position_50_02']
    )
    tiprack_50_3 = protocol.load_labware(
        load_name=config['tip_rack_type_50_03'], location=config['tip_rack_position_50_03']
    )


    # Pipettes
    p50 = protocol.load_instrument('flex_8channel_50', mount='right', tip_racks=[tiprack_50_1, tiprack_50_2, tiprack_50_3])
    p50s = protocol.load_instrument('flex_1channel_50', mount='left', tip_racks=[tiprack_50_1, tiprack_50_2, tiprack_50_3])

    p50.configure_nozzle_layout(style='COLUMN', start='A1', tip_racks=[tiprack_50_1, tiprack_50_2, tiprack_50_3])
    # p50s.configure_nozzle_layout(style=SINGLE, start='A1', tip_racks=[tiprack_200])



    # Perform combinatorial transfers #TODO: SWAP?  so adding small vols into large quant of master mix
    sybrgreen_to_dest(protocol=protocol,
                      reagent_plate=reagent_plate,
                      sybrgreen_plate=sybrgreen_plate,
                      pipette=p50,
                      config=config)

    pcr_to_dest(protocol=protocol,
                pcr_plate=pcr_plate,
                sybrgreen_plate=sybrgreen_plate,
                pipette=p50,
                config=config)
    
    water_to_pcr_dilution_wells(protocol=protocol,
                                diluted_pcr=diluted_pcr_plate,
                                reagent_plate=reagent_plate,
                                pipette=p50,
                                config=config)
    
    pcr_to_water(protocol=protocol,
                 pcr_plate=pcr_plate,
                 diluted_pcr=diluted_pcr_plate,
                 pipette=p50,
                 config=config)
    
    
    controls_to_pcr(protocol=protocol,
                    diluted_pcr=diluted_pcr_plate,
                    controls_plate=controls_plate,
                    pipette=p50s,
                    config=config)


