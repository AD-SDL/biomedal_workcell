from opentrons import protocol_api
from opentrons.protocol_api import SINGLE

metadata = {
    'protocolName': 'move B2 to A4',
    'author': 'Abe Stroka',
    'description': 'Automated Golden Gate Assembly using OT-Flex',
}

requirements = {"robotType": "Flex", "apiLevel": "2.20"}

def run(protocol: protocol_api.ProtocolContext):
    # Labware
    # source_plate = protocol.load_labware('nest_96_wellplate_200ul_flat', 'B1')
    # pcr_plate = protocol.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', 'C2')
    pcr_plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 'A4')
    mastermix_tube = protocol.load_labware('nest_12_reservoir_15ml', 'B3') #TODO change
    water_reservoir = protocol.load_labware('nest_12_reservoir_15ml', 'A1')
    temp_mod = protocol.load_module(module_name="temperature module gen2", location="C1")
    temp_adapter = temp_mod.load_adapter("opentrons_96_well_aluminum_block")
    dna = temp_adapter.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')
    temp_mod2 = protocol.load_module(module_name="temperature module gen2", location="B1")
    temp_adapter2 = temp_mod2.load_adapter("opentrons_96_well_aluminum_block")
    dna2 = temp_adapter2.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')

    tiprack_50 = protocol.load_labware(
        load_name="opentrons_flex_96_tiprack_50ul", location="A2",
    )





    # Pipettes
    p50 = protocol.load_instrument('flex_8channel_50', mount='right', tip_racks=[tiprack_50])



    # load trash bin
    # _ = protocol.load_trash_bin("D1")
    chute = protocol.load_waste_chute()

    protocol.move_labware(labware=pcr_plate, new_location="C2", use_gripper=True)