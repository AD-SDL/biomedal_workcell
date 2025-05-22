from opentrons import protocol_api

# metadata
metadata = {
    "protocolName": "Plate dispsene media",
    "author": "Casey Stone",
    "description": "Prep protocol for 2 plate substrate experiment",
}

# requirements
requirements = {"robotType": "OT-2", "apiLevel": "2.12"}


# protocol run function
def run(protocol: protocol_api.ProtocolContext):
    # * load labware
    substrate_stock = protocol.load_labware(
        "nest_96_wellplate_2ml_deep",
        location="4",
    )

    substrate_assay_plate_1 = protocol.load_labware(
        "corning_96_wellplate_360ul_flat",
        location="7",
    )
    substrate_assay_plate_2 = protocol.load_labware(
        "corning_96_wellplate_360ul_flat",
        location="8",
    )
    substrate_assay_plate_3 = protocol.load_labware(
        "corning_96_wellplate_360ul_flat",
        location="9",
    )
    substrate_assay_plate_4 = protocol.load_labware(
        "corning_96_wellplate_360ul_flat",
        location="10",
    )
    substrate_assay_plate_5 = protocol.load_labware(
        "corning_96_wellplate_360ul_flat",
        location="11",
    )

    tip_rack_300uL = protocol.load_labware(
        "opentrons_96_filtertiprack_200ul",
        location="6",
    )

    # set labware offsets
    tip_rack_300uL.set_offset(x=0.4, y=1.1, z=0.0)  # pos 6
    substrate_stock.set_offset(x=-0.0, y=0.3, z=0.0)  # pos 4
    substrate_assay_plate_1.set_offset(x=-0.0, y=1.0, z=0.0)  # pos 7
    substrate_assay_plate_2.set_offset(x=-0.0, y=0.0, z=0.0)  # pos 8
    substrate_assay_plate_3.set_offset(x=-0.0, y=0.3, z=0.0)  # pos 9
    substrate_assay_plate_4.set_offset(x=-0.0, y=0.4, z=0.0)  # pos 10
    substrate_assay_plate_5.set_offset(x=-0.0, y=0.2, z=0.0)  # pos 11

    # variables
    media_transfer_volume = 180

    # * load pipettes
    right_pipette_300uL_multi = protocol.load_instrument(
        "p300_multi_gen2", mount="right", tip_racks=[tip_rack_300uL]
    )

    # * commands
    # Step 1: Transfer 150uL from one column of substrate plate into all columns of assay plate. Repeat for all assay plates.
    substrate_assay_plates = [
        substrate_assay_plate_1,
        substrate_assay_plate_2,
        substrate_assay_plate_3,
        substrate_assay_plate_4,
        substrate_assay_plate_5,
    ]

    # Dispense blanks into column 1 of all substrate plates
    right_pipette_300uL_multi.pick_up_tip()
    destination_columns = [plate.columns()[0] for plate in substrate_assay_plates]
    right_pipette_300uL_multi.distribute(
        media_transfer_volume, 
        substrate_stock.columns()[5],
        destination_columns, 
        new_tip="never", 
        disposal_volume = 0,
    )

    # Dispense blanks into column 12 of all substrate plates
    destination_columns = [plate.columns()[11] for plate in substrate_assay_plates]
    right_pipette_300uL_multi.distribute(
        media_transfer_volume, 
        substrate_stock.columns()[11],
        destination_columns, 
        new_tip="never", 
        disposal_volume = 0,
    )
    right_pipette_300uL_multi.drop_tip()

    # Dispense stock media into first half of each substrate plate
    right_pipette_300uL_multi.pick_up_tip()
    for i in range(5): 
        destination_columns = substrate_assay_plates[i].columns()[1:6]   # means columns 2-6
        right_pipette_300uL_multi.distribute(
            media_transfer_volume,
            substrate_stock.columns()[i],
            [column[0] for column in destination_columns],
            new_tip = "never", 
            disposal_volume = 0,
        )
    right_pipette_300uL_multi.drop_tip()

    # Dispense stock media into second half of each substrate plate
    right_pipette_300uL_multi.pick_up_tip()
    for i in range(5): 
        destination_columns = substrate_assay_plates[i].columns()[6:11]   # means columns 7-11
        right_pipette_300uL_multi.distribute(
            media_transfer_volume,
            substrate_stock.columns()[i+6],
            [column[0] for column in destination_columns],
            new_tip = "never", 
            disposal_volume = 0,
        )
    right_pipette_300uL_multi.drop_tip()