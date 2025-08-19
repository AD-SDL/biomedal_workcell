requirements = {"robotType": "OT-2"}

from opentrons import protocol_api


metadata = {
    "protocolName": "NA",
    "author": "Autoprotocol",
    "description": "NA",
    "apiLevel": "2.12",
    "info": "A PCR protocol written by Autoprotocol",
    "name": "Test Protocol",
    "version": "0.1"
}

def run(protocol: protocol_api.ProtocolContext):

    deck = {}
    pipettes = {}


    ################
    # load labware #
    ################
    module = protocol.load_module("Temperature Module", "3")
    deck["3"] = module.load_labware("nest_96_wellplate_100ul_pcr_full_skirt")

    deck["3"].set_offset(x=1.0, y=1.6, z=11.0)

    deck["1"] = protocol.load_labware("nest_96_wellplate_100ul_pcr_full_skirt", "1")

    deck["1"].set_offset(x=0.0, y=1.7, z=3.9)

    deck["7"] = protocol.load_labware("opentrons_96_tiprack_20ul", "7")

    deck["7"].set_offset(x=0.2, y=0.4, z=0.0)

    pipettes["left"] = protocol.load_instrument("p20_single_gen2", "left", tip_racks=[deck["7"]])


    ####################
    # execute commands #
    ####################

    # transfer 20 uL qPCR Master Mix from react_plate well A1 to dest_plate wells B2 and B11
    pipettes["left"].pick_up_tip(deck["7"].wells()[0])

    pipettes["left"].well_bottom_clearance.aspirate = 1

    pipettes["left"].aspirate(20.0, deck["3"]["A1"])

    pipettes["left"].well_bottom_clearance.dispense = 1

    pipettes["left"].dispense(20.0, deck["1"]["B2"])

    pipettes["left"].blow_out()

    pipettes["left"].drop_tip()


    pipettes["left"].pick_up_tip(deck["7"].wells()[1])

    pipettes["left"].well_bottom_clearance.aspirate = 1

    pipettes["left"].aspirate(20.0, deck["3"]["A2"])

    pipettes["left"].well_bottom_clearance.dispense = 1

    pipettes["left"].dispense(20.0, deck["1"]["B11"])

    pipettes["left"].blow_out()

    pipettes["left"].drop_tip()


    pipettes["left"].pick_up_tip(deck["7"].wells()[2])

    pipettes["left"].well_bottom_clearance.aspirate = 1

    pipettes["left"].aspirate(20.0, deck["3"]["A1"])

    pipettes["left"].well_bottom_clearance.dispense = 1

    pipettes["left"].dispense(20.0, deck["1"]["G2"])

    pipettes["left"].blow_out()

    pipettes["left"].drop_tip()


    pipettes["left"].pick_up_tip(deck["7"].wells()[3])

    pipettes["left"].well_bottom_clearance.aspirate = 1

    pipettes["left"].aspirate(20.0, deck["3"]["A2"])

    pipettes["left"].well_bottom_clearance.dispense = 1

    pipettes["left"].dispense(20.0, deck["1"]["G11"])

    pipettes["left"].blow_out()

    pipettes["left"].drop_tip()



    # transfer 5 uL Nuclease-free Biowater from react_plate well C1 to dest_plate B2 and B11
    pipettes["left"].pick_up_tip(deck["7"].wells()[4])

    pipettes["left"].well_bottom_clearance.aspirate = 1

    pipettes["left"].aspirate(5.0, deck["3"]["C1"])

    pipettes["left"].well_bottom_clearance.dispense = 1

    pipettes["left"].dispense(5.0, deck["1"]["B2"])

    pipettes["left"].blow_out()

    pipettes["left"].drop_tip()


    pipettes["left"].pick_up_tip(deck["7"].wells()[5])

    pipettes["left"].well_bottom_clearance.aspirate = 1

    pipettes["left"].aspirate(5.0, deck["3"]["C2"])

    pipettes["left"].well_bottom_clearance.dispense = 1

    pipettes["left"].dispense(5.0, deck["1"]["B11"])

    pipettes["left"].blow_out()

    pipettes["left"].drop_tip()


    pipettes["left"].pick_up_tip(deck["7"].wells()[6])

    pipettes["left"].well_bottom_clearance.aspirate = 1

    pipettes["left"].aspirate(5.0, deck["3"]["C3"])

    pipettes["left"].well_bottom_clearance.dispense = 1

    pipettes["left"].dispense(5.0, deck["1"]["G2"])

    pipettes["left"].blow_out()

    pipettes["left"].drop_tip()


    pipettes["left"].pick_up_tip(deck["7"].wells()[7])

    pipettes["left"].well_bottom_clearance.aspirate = 1

    pipettes["left"].aspirate(5.0, deck["3"]["C4"])

    pipettes["left"].well_bottom_clearance.dispense = 1

    pipettes["left"].dispense(5.0, deck["1"]["G11"])

    pipettes["left"].blow_out()

    pipettes["left"].drop_tip()



    # transfer 5 uL Forward Primer from react_plate D1 to dest_plate B2 and B11
    pipettes["left"].pick_up_tip(deck["7"].wells()[8])

    pipettes["left"].well_bottom_clearance.aspirate = 1

    pipettes["left"].aspirate(5.0, deck["3"]["D1"])

    pipettes["left"].well_bottom_clearance.dispense = 1

    pipettes["left"].dispense(5.0, deck["1"]["B2"])

    pipettes["left"].blow_out()

    pipettes["left"].drop_tip()


    pipettes["left"].pick_up_tip(deck["7"].wells()[9])

    pipettes["left"].well_bottom_clearance.aspirate = 1

    pipettes["left"].aspirate(5.0, deck["3"]["D1"])

    pipettes["left"].well_bottom_clearance.dispense = 1

    pipettes["left"].dispense(5.0, deck["1"]["B11"])

    pipettes["left"].blow_out()

    pipettes["left"].drop_tip()


    pipettes["left"].pick_up_tip(deck["7"].wells()[10])

    pipettes["left"].well_bottom_clearance.aspirate = 1

    pipettes["left"].aspirate(5.0, deck["3"]["D1"])

    pipettes["left"].well_bottom_clearance.dispense = 1

    pipettes["left"].dispense(5.0, deck["1"]["G2"])

    pipettes["left"].blow_out()

    pipettes["left"].drop_tip()


    pipettes["left"].pick_up_tip(deck["7"].wells()[10])

    pipettes["left"].well_bottom_clearance.aspirate = 1

    pipettes["left"].aspirate(5.0, deck["3"]["D1"])

    pipettes["left"].well_bottom_clearance.dispense = 1

    pipettes["left"].dispense(5.0, deck["1"]["G11"])

    pipettes["left"].blow_out()

    pipettes["left"].drop_tip()



    # transfer 5 uL of Reverse Primer from react_plate E1 to dest_plate B2 and B11
    pipettes["left"].pick_up_tip(deck["7"].wells()[10])

    pipettes["left"].well_bottom_clearance.aspirate = 1

    pipettes["left"].aspirate(5.0, deck["3"]["E1"])

    pipettes["left"].well_bottom_clearance.dispense = 1

    pipettes["left"].dispense(5.0, deck["1"]["B2"])

    pipettes["left"].blow_out()

    pipettes["left"].drop_tip()


    pipettes["left"].pick_up_tip(deck["7"].wells()[10])

    pipettes["left"].well_bottom_clearance.aspirate = 1

    pipettes["left"].aspirate(5.0, deck["3"]["E1"])

    pipettes["left"].well_bottom_clearance.dispense = 1

    pipettes["left"].dispense(5.0, deck["1"]["B11"])

    pipettes["left"].blow_out()

    pipettes["left"].drop_tip()


    pipettes["left"].pick_up_tip(deck["7"].wells()[10])

    pipettes["left"].well_bottom_clearance.aspirate = 1

    pipettes["left"].aspirate(5.0, deck["3"]["E1"])

    pipettes["left"].well_bottom_clearance.dispense = 1

    pipettes["left"].dispense(5.0, deck["1"]["G2"])

    pipettes["left"].blow_out()

    pipettes["left"].drop_tip()


    pipettes["left"].pick_up_tip(deck["7"].wells()[10])

    pipettes["left"].well_bottom_clearance.aspirate = 1

    pipettes["left"].aspirate(5.0, deck["3"]["E1"])

    pipettes["left"].well_bottom_clearance.dispense = 1

    pipettes["left"].dispense(5.0, deck["1"]["G11"])

    pipettes["left"].blow_out()

    pipettes["left"].drop_tip()



    # transfer 5 uL of Template DNA from react_plate H1 to dest_plate B2
    pipettes["left"].pick_up_tip(deck["7"].wells()[10])

    pipettes["left"].well_bottom_clearance.aspirate = 1

    pipettes["left"].aspirate(5.0, deck["3"]["H1"])

    pipettes["left"].well_bottom_clearance.dispense = 1

    pipettes["left"].dispense(5.0, deck["1"]["B2"])

    pipettes["left"].blow_out()

    pipettes["left"].drop_tip()


    pipettes["left"].pick_up_tip(deck["7"].wells()[10])

    pipettes["left"].well_bottom_clearance.aspirate = 1

    pipettes["left"].aspirate(5.0, deck["3"]["H1"])

    pipettes["left"].well_bottom_clearance.dispense = 1

    pipettes["left"].dispense(5.0, deck["1"]["G2"])

    pipettes["left"].blow_out()

    pipettes["left"].drop_tip()



    # transfer 5 uL Nuclease-free Biowater from react_plate well C1 to dest_plate B11
    pipettes["left"].pick_up_tip(deck["7"].wells()[10])

    pipettes["left"].well_bottom_clearance.aspirate = 1

    pipettes["left"].aspirate(5.0, deck["3"]["C2"])

    pipettes["left"].well_bottom_clearance.dispense = 1

    pipettes["left"].dispense(5.0, deck["1"]["B11"])

    pipettes["left"].blow_out()

    pipettes["left"].drop_tip()


    pipettes["left"].pick_up_tip(deck["7"].wells()[10])

    pipettes["left"].well_bottom_clearance.aspirate = 1

    pipettes["left"].aspirate(5.0, deck["3"]["C4"])

    pipettes["left"].well_bottom_clearance.dispense = 1

    pipettes["left"].dispense(5.0, deck["1"]["G11"])

    pipettes["left"].blow_out()

    pipettes["left"].drop_tip()



    # Mix 10X with pipet set to 36ul
    pipettes["left"].pick_up_tip(deck["7"].wells()[10])

    pipettes["left"].well_bottom_clearance.aspirate = 1

    pipettes["left"].aspirate(1.0, deck["3"]["B2"])

    pipettes["left"].well_bottom_clearance.dispense = 1

    pipettes["left"].dispense(1.0, deck["1"]["B2"])

    pipettes["left"].mix(10, 20, deck["1"]["B2"])

    pipettes["left"].blow_out()

    pipettes["left"].drop_tip()


    pipettes["left"].pick_up_tip(deck["7"].wells()[10])

    pipettes["left"].well_bottom_clearance.aspirate = 1

    pipettes["left"].aspirate(1.0, deck["3"]["G2"])

    pipettes["left"].well_bottom_clearance.dispense = 1

    pipettes["left"].dispense(1.0, deck["1"]["G2"])

    pipettes["left"].mix(10, 20, deck["1"]["G2"])

    pipettes["left"].blow_out()

    pipettes["left"].drop_tip()


    pipettes["left"].pick_up_tip(deck["7"].wells()[10])

    pipettes["left"].well_bottom_clearance.aspirate = 1

    pipettes["left"].aspirate(1.0, deck["3"]["B11"])

    pipettes["left"].well_bottom_clearance.dispense = 1

    pipettes["left"].dispense(1.0, deck["1"]["B11"])

    pipettes["left"].mix(10, 20, deck["1"]["B11"])

    pipettes["left"].blow_out()

    pipettes["left"].drop_tip()


    pipettes["left"].pick_up_tip(deck["7"].wells()[10])

    pipettes["left"].well_bottom_clearance.aspirate = 1

    pipettes["left"].aspirate(1.0, deck["3"]["G11"])

    pipettes["left"].well_bottom_clearance.dispense = 1

    pipettes["left"].dispense(1.0, deck["1"]["G11"])

    pipettes["left"].mix(10, 20, deck["1"]["G11"])

    pipettes["left"].blow_out()

    pipettes["left"].drop_tip()

