requirements = {"robotType": "Flex"}

from opentrons import protocol_api


metadata = {
    "protocolName": "Load A4 to temp module",
    "author": "Abe astroka@anl.gov",
    "description": "pd cfpe assay",
    "apiLevel": "2.18"
}

def run(protocol: protocol_api.ProtocolContext):

    deck = {}
    pipettes = {}


    ################
    # load labware #
    ################
    deck["A4"] = protocol.load_labware("nest_96_wellplate_100ul_pcr_full_skirt", "A4")

    module = protocol.load_module("temperature module gen2", "C1")
    # deck["C1"] = module.load_labware("nest_96_wellplate_100ul_pcr_full_skirt")

    # deck["C1"].set_offset(x=1.0, y=1.6, z=11.0)
    # adapter = module.load_adapter("opentrons_96_flat_bottom_adapter")

    deck["A1"] = protocol.load_trash_bin("A1")

    pipettes["right"] = protocol.load_instrument("flex_8channel_50", "right", tip_racks=[])

    pipettes["left"] = protocol.load_instrument("flex_1channel_1000", "left", tip_racks=[])


    ####################
    # execute commands #
    ####################

    # move_test
    # module.open_labware_latch()
    protocol.move_labware(labware=deck["A4"], new_location=module, use_gripper=True)
