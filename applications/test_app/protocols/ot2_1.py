from opentrons import protocol_api

# metadata
metadata = {
    "protocolName": "Demo protocol 1",
    "author": "Name <opentrons@example.com>",
    "description": "Demo protocol 1",
}

# requirements
requirements = {"robotType": "OT-2", "apiLevel": "2.19"}


# protocol run function
def run(protocol: protocol_api.ProtocolContext):
    # labware
    plate = protocol.load_labware("corning_96_wellplate_360ul_flat", location="1")
    reservoir = protocol.load_labware("nest_12_reservoir_15ml", location="10")
    tiprack = protocol.load_labware("opentrons_96_tiprack_300ul", location="11")
    tiprack.set_offset(x=-0.7, y=0.3, z=0.0)

    # pipettes
    left_pipette = protocol.load_instrument(
        "p300_single_gen2", mount="left", tip_racks=[tiprack]
    )

    # commands
    left_pipette.pick_up_tip(tiprack["A1"])

    left_pipette.aspirate(100, reservoir["A1"])
    left_pipette.dispense(100, plate["A1"])

    left_pipette.aspirate(100, reservoir["A1"])
    left_pipette.dispense(100, plate["A2"])

    left_pipette.aspirate(100, reservoir["A1"])
    left_pipette.dispense(100, plate["A3"])

    left_pipette.drop_tip()
