from opentrons import protocol_api

# TODO: TEST!!!!
# TODO: HOW TO SUBSTITUTE VARIABLES!

# metadata
metadata = {
    "protocolName": "Inoculate Protocol for 2 plate substrate experiment",
    "author": "Casey Stone",
    "description": "OT-2 protocol for inoculating whole substrate plate",
}

# requirements
requirements = {"robotType": "OT-2", "apiLevel": "2.12"}


# protocol run function
def run(protocol: protocol_api.ProtocolContext):


    # load substrate plates
    substrate_assay_plate_new = protocol.load_labware(
        "corning_96_wellplate_360ul_flat",
        location="1",
    )
    substrate_assay_plate_old = protocol.load_labware(
        "corning_96_wellplate_360ul_flat",
        location="3",
    )

    tip_rack= protocol.load_labware(
        "opentrons_96_tiprack_20ul",
        location="$tip_location",
    )

    # load tip racks
    # tip_rack_1 = protocol.load_labware(
    #     "opentrons_96_tiprack_20ul",
    #     location="4",
    # )
    # tip_rack_2 = protocol.load_labware(
    #     "opentrons_96_tiprack_20ul",
    #     location="5",
    # )
    # tip_rack_3 = protocol.load_labware(
    #     "opentrons_96_tiprack_20ul",
    #     location="6",
    # )
    # tip_rack_4 = protocol.load_labware(
    #     "opentrons_96_tiprack_20ul",
    #     location="7",
    # )
    # tip_rack_5 = protocol.load_labware(
    #     "opentrons_96_tiprack_20ul",
    #     location="8",
    # )
    # tip_rack_6 = protocol.load_labware(
    #     "opentrons_96_tiprack_20ul",
    #     location="9",
    # )
    # tip_rack_7 = protocol.load_labware(
    #     "opentrons_96_tiprack_20ul",
    #     location="10",
    # )
    # tip_rack_8 = protocol.load_labware(
    #     "opentrons_96_tiprack_20ul",
    #     location="11",
    # )


    tip_rack.set_offset(x=float("$x"), y=float("$y"), z=float("$z")) 

    # set labware offsets
    # tip_rack_1.set_offset(x=-0.0, y=0.3, z=0.0)  # pos 4
    # tip_rack_2.set_offset(x=0.4, y=0.4, z=-0.5)  # pos 5
    # tip_rack_3.set_offset(x=0.4, y=1.1, z=0.0)  # pos 6
    # tip_rack_4.set_offset(x=-0.0, y=1.0, z=0.0)  # pos 7
    # tip_rack_5.set_offset(x=0.0,y=0.0,z=0.0)   # pos 8
    # tip_rack_6.set_offset(x=-0.0, y=0.3, z=0.0)  # pos 9
    # tip_rack_7.set_offset(x=0.1,y=1.0,z=0.0)  # pos 10
    # tip_rack_8.set_offset(x=0.2,y=0.3,z=0.0)   # pos 11

    substrate_assay_plate_new.set_offset(x=0.0,y=2.0,z=0.0)  # pos 1
    substrate_assay_plate_old.set_offset(x=0.0,y=0.5,z=0.0)   # pos 3

    # variables
    inoculation_volume = 5

    # * load pipettes
    # left_pipette_20uL_multi = protocol.load_instrument(
    #     "p20_multi_gen2", mount="left", tip_racks=[
    #         tip_rack_1, 
    #         tip_rack_2, 
    #         tip_rack_3, 
    #         tip_rack_4, 
    #         tip_rack_5, 
    #         tip_rack_6, 
    #         tip_rack_7, 
    #         tip_rack_8]
    # )
    left_pipette_20uL_multi = protocol.load_instrument(
        "p20_multi_gen2", mount="left", tip_racks=[
            tip_rack, 
        ]
    )

    # COMMANDS ------------------
    # Inoculate new substrate plate from old substrate plate 
    source_columns = substrate_assay_plate_old.columns()[0:12]   # means all columns 1-12
    destination_columns = substrate_assay_plate_new.columns()[0:12]  # means all columns 1-12
    left_pipette_20uL_multi.transfer(
        inoculation_volume, 
        source_columns, 
        destination_columns, 
        new_tip="always",
        disposal_volume = 0, 
        # mix_before=(3, 20), # mix 3 times with 20ul before transfer 
        # mix_after=(3, 20)  # mix 3 times with 20ul after transfer 
    )


