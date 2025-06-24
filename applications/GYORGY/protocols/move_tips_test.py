from opentrons import protocol_api

# metadata
metadata = {
    "protocolName": "My Protocol",
    "author": "Name <opentrons@example.com>",
    "description": "Simple protocol to get started using the Flex",
}

# requirements
requirements = {"robotType": "Flex", "apiLevel": "2.23"}

# protocol run function
def run(protocol: protocol_api.ProtocolContext):
    # labware
    plate = protocol.load_labware(
        "corning_96_wellplate_360ul_flat", location="D1"
    )
    tiprack = protocol.load_labware(
        "opentrons_flex_96_filtertiprack_50ul", location="A4"
    )
    chute = protocol.load_waste_chute()

    # pipettes
    right_pipette = protocol.load_instrument(
        "flex_8channel_50", mount="right", tip_racks=[tiprack]
    )

    # commands
    protocol.move_labware(labware=tiprack, new_location="A1")

    # right_pipette.pick_up_tip()
    # right_pipette.aspirate(100, plate["A1"])
    # right_pipette.dispense(100, plate["B2"])
    # right_pipette.drop_tip()