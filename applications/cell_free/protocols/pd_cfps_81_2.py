from opentrons import protocol_api
import itertools
from opentrons.protocol_api import SINGLE


metadata = {
    'protocolName': 'Protein Design CFPS part 2',
    'author': 'LDRD team ',
    'description': 'CFPS plate setup from PCR templates and standards followed by CFPS on the deck',
    'source': 'FlexAS/pd_cfps_81_2.py'
}

requirements = {"robotType": "Flex", "apiLevel": "2.20"}

config = {
    'combinations': [[18,10,2],[11,19,3],[4,20,12],[21,13,5]], # 1-indexed source well numbers (kept for total calculation)
    'temperature' : 4,

    'heater_shaker_temp': 37,     # °C for heater/shaker
    'shaking_duration': 150,      # minutes (2.5 hours) for shaking (CFPS)
    'shaking_speed': 200,

    'rmf_plate_type': 'nest_96_wellplate_100ul_pcr_full_skirt',
    'diluted_pcr_plate_type': 'nest_96_wellplate_100ul_pcr_full_skirt',
    'cfps_plate_type': 'nest_96_wellplate_100ul_pcr_full_skirt',
    'tip_rack_type_50_01': 'opentrons_flex_96_tiprack_50ul',
    'tip_rack_type_50_02': 'opentrons_flex_96_tiprack_50ul',
    'tip_rack_type_50_03': 'opentrons_flex_96_tiprack_50ul',
    'reagent_plate_type': 'nest_12_reservoir_15ml',
    'pcr_adapter_type': 'opentrons_96_pcr_adapter',
    'sealed_plate_type': 'nest_96_wellplate_100ul_pcr_full_skirt',

    'rmf_plate_position': 'B1',
    'diluted_pcr_plate_position': 'C1',
    'cfps_plate_position': 'C2',
    'temp_module_01_position': 'B1',
    'temp_module_02_position': 'C1',
    'tip_rack_position_50_01': 'A2',
    'tip_rack_position_50_02': 'A3',
    'tip_rack_position_50_03': 'B3',
    'reagent_plate_position': 'A1',
    'shaker_module_position': 'D1',
    'sealed_plate_position': 'A4'

}


def run(protocol: protocol_api.ProtocolContext):
    # Load temperature module and adapter
    temp_mod1 = protocol.load_module(module_name="temperature module gen2", location=config['temp_module_01_position'])
    temp_adapter1 = temp_mod1.load_adapter("opentrons_96_well_aluminum_block")

    temp_mod2 = protocol.load_module(module_name="temperature module gen2", location=config['temp_module_02_position'])
    temp_adapter2 = temp_mod2.load_adapter("opentrons_96_well_aluminum_block")

    # Set temperature
    temp_mod1.set_temperature(config['temperature']) #TODO: make seperate, or just set earlier, only 1 hour with plate
    temp_mod2.set_temperature(config['temperature']) #TODO: make seperate, or just set earlier, only 1 hour with plate

    shaker_mod = protocol.load_module(module_name="heaterShakerModuleV1", location=config['shaker_module_position'])
    shaker_adapter = shaker_mod.load_adapter(config['pcr_adapter_type'])
    shaker_mod.set_target_temperature(config['heater_shaker_temp'])

    # shaker_mod.open_labware_latch()

    chute = protocol.load_waste_chute()

    rmf_plate = temp_adapter1.load_labware(config['rmf_plate_type'])
    rmf_plate.set_offset(x=0.40, y=0.50, z=2.40)

    diluted_pcr_plate = temp_adapter2.load_labware(config['diluted_pcr_plate_type'])
    diluted_pcr_plate.set_offset(x=0.40, y=0.50, z=2.40)

    cfps_plate = protocol.load_labware(config['cfps_plate_type'], config['cfps_plate_position'])
    cfps_plate.set_offset(x=0.4, y=0.4, z=0.0)

    tiprack_50_1 = protocol.load_labware(
        load_name=config['tip_rack_type_50_01'], location=config['tip_rack_position_50_01']
    )
    tiprack_50_2 = protocol.load_labware(
        load_name=config['tip_rack_type_50_02'], location=config['tip_rack_position_50_02']
    )
    tiprack_50_3 = protocol.load_labware(
        load_name=config['tip_rack_type_50_03'], location=config['tip_rack_position_50_03']
    )

    sealed_plate = protocol.load_labware(config['sealed_plate_type'], config['sealed_plate_position'])

    # Pipettes
    p50 = protocol.load_instrument('flex_8channel_50', mount='right', tip_racks=[tiprack_50_1, tiprack_50_2, tiprack_50_3])
    p50s = protocol.load_instrument('flex_1channel_50', mount='left', tip_racks=[tiprack_50_1, tiprack_50_2, tiprack_50_3])

    p50.configure_nozzle_layout(style='COLUMN', start='A1', tip_racks=[tiprack_50_1, tiprack_50_2, tiprack_50_3])

    shaker_mod.open_labware_latch()

    protocol.move_labware(
        labware=sealed_plate,
        new_location=shaker_adapter,
        use_gripper=True
    )

    shaker_mod.close_labware_latch()

    shaker_mod.set_and_wait_for_shake_speed(config['shaking_speed'])
    protocol.delay(minutes=config['shaking_duration'])
    protocol.comment("Stopping shaking")
    shaker_mod.deactivate_shaker()

    shaker_mod.open_labware_latch()

    protocol.comment("Moving reaction plate from heater/shaker back to A4 for peeling")
    protocol.move_labware(
        labware=sealed_plate,
        new_location=config['sealed_plate_position'],
        use_gripper=True
    )