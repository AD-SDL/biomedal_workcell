from opentrons import protocol_api

# metadata
metadata = {
    "protocolName": "Plate Prep and First Inoculation",
    "author": "Casey Stone",
    "description": "First protocol in Substrate app",
}

# requirements
requirements = {"robotType": "OT-2", "apiLevel": "2.12"}


# protocol run function
def run(protocol: protocol_api.ProtocolContext):
    # TODOs:
    # do we need to use a disposal volume for propper liquid transfers?
    # we may need to change the z height aspirating from source substrate deepwell overtime
    # do we have enough volume in the substrate deepwell
    # add labware offsets to each deck position

    # * load labware
    substrate_stock = protocol.load_labware(
        "nest_96_wellplate_2ml_deep",
        location="4",
    )

    substrate_assay_plate_1 = protocol.load_labware(
        "corning_96_wellplate_360ul_flat",
        location="1",
    )
    substrate_assay_plate_2 = protocol.load_labware(
        "corning_96_wellplate_360ul_flat",
        location="7",
    )
    substrate_assay_plate_3 = protocol.load_labware(
        "corning_96_wellplate_360ul_flat",
        location="8",
    )
    substrate_assay_plate_4 = protocol.load_labware(
        "corning_96_wellplate_360ul_flat",
        location="9",
    )
    substrate_assay_plate_5 = protocol.load_labware(
        "corning_96_wellplate_360ul_flat",
        location="10",
    )
    substrate_assay_plate_6 = protocol.load_labware(
        "corning_96_wellplate_360ul_flat",
        location="11",
    )

    tip_rack_300uL = protocol.load_labware(
        "opentrons_96_filtertiprack_200ul",
        location="5",
    )
    tip_rack_20uL = protocol.load_labware(
        "opentrons_96_tiprack_20ul",
        location="6",
    )

    # set labware offsets
    tip_rack_300uL.set_offset(x=0.1, y=0.4, z=-0.5)  # pos 5
    tip_rack_20uL.set_offset(x=0.4, y=1.1, z=0.0)  # pos 6
    substrate_assay_plate_1.set_offset(x=-0.0, y=1.2, z=0.0)  # pos 1
    substrate_assay_plate_2.set_offset(x=-0.0, y=1.0, z=0.0)  # pos 7
    substrate_assay_plate_3.set_offset(x=-0.0, y=0.0, z=0.0)  # pos 8
    substrate_assay_plate_4.set_offset(x=-0.0, y=0.3, z=0.0)  # pos 9
    substrate_assay_plate_5.set_offset(x=-0.0, y=0.4, z=0.0)  # pos 10
    substrate_assay_plate_6.set_offset(x=-0.0, y=0.2, z=0.0)  # pos 11

    # * load pipettes
    left_pipette_20uL_multi = protocol.load_instrument(
        "p20_multi_gen2", mount="left", tip_racks=[tip_rack_20uL]
    )
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
        substrate_assay_plate_6,
    ]
    for i in range(len(substrate_assay_plates)):
        source_column = substrate_stock.columns_by_name()[str(i + 1)]
        destination_columns = substrate_assay_plates[i].columns()
        right_pipette_300uL_multi.distribute(
            150,
            source_column[0],
            [column[0] for column in destination_columns],
            new_tip="once",
            disposal_volume=0,  # TODO: do we need a disposal volume for propper volume transfer
        )

    # Inoculate 3 columns (columns 1, 5, and 9) of assay plate 1 from substrate stock plate columns 8, 10, and 12 respectively
    left_pipette_20uL_multi.pick_up_tip()
    left_pipette_20uL_multi.aspirate(5, substrate_stock["A8"])
    left_pipette_20uL_multi.dispense(5, substrate_assay_plate_1["A1"])
    left_pipette_20uL_multi.drop_tip()

    left_pipette_20uL_multi.pick_up_tip()
    left_pipette_20uL_multi.aspirate(5, substrate_stock["A10"])
    left_pipette_20uL_multi.dispense(5, substrate_assay_plate_1["A5"])
    left_pipette_20uL_multi.drop_tip()

    left_pipette_20uL_multi.pick_up_tip()
    left_pipette_20uL_multi.aspirate(5, substrate_stock["A12"])
    left_pipette_20uL_multi.dispense(5, substrate_assay_plate_1["A9"])
    left_pipette_20uL_multi.drop_tip()
