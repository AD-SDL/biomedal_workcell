# biomedal-workcell

This is a repository for the biology robotic Workcell in building 446.

### Nodes availible
- Opentrons OT-Flex
- Opentrons OT-2 (two available)
- Precise Flex PF400 Robotic Arm
- Analytik Jena Biometra Thermal Cyclers (96 and 384-well versions)
- BMG VANTAstar Microplate Reader
- Hidex Sense Microplate Reader
- Azenta Automated Microplate Sealer
- Azenta Automated Plate Seal Remover
- BioNex Solutions HiG4 Automated Centrifuge (FUTURE)


### Current projects
- MEDAL, led by Arvind Ramanathan
- Adaptive Lab Evolution, led by Nidhi Gupta
- Autonomous Protein Design, led by Gyorgy Babnigg and Rose Wilton.

## Dependencies

- You'll need [docker installed](https://docs.docker.com/engine/install/)
    - Make sure on Linux to follow the [post installation steps](https://docs.docker.com/engine/install/linux-postinstall/) to enable non-root user access
- You'll need Python 3.8 or greater installed to run the Experiment Applications.

## Configuration

As much as possible, this workcell is designed to be configured declaratively. This is done with:

- A `.env` file, which you can create by copying `example.env` (`cp example.env .env` on Linux), or by running `make init`.
    - After creating the `.env`, check to make sure the values are complete and correct.
- The `compose.yaml` docker compose file, which defines a "stack" of containers that control your workcell
    - Note: whenever you see `${SOME_VARIABLE_NAME}` in the compose file, this value is being taken from the `.env`
- The Workcell Config in `workcell_defs/example_workcell.yaml`, which allows you to define WEI specific configuration for your workcell

## Building, Running, and Managing your Workcell

### General Instructions
- `make init` to initialize your `.env` file (check to see that the values are correct)
- `docker compose up` to start your workcell (`docker compose up -d` starts it in the background)
- `docker compose down` to stop a workcell
- `docker compose logs -f` to view the output

### Specific instructions for the Biomedal Workcell

#### Start nodes running through Windows Powershell

Hidex Sense Microplate Reader: TODO

Biometra Thermocyclers (96 and 384 well versions): TODO

BMG VANTAstar microplate reader: TODO

Sealer: TODO

Peeler: TODO

#### Start the rest of the nodes and wei service through WSL terminal.

1. open a wsl terminal
2. cd into the biomedal_workcell folder

        cd biomedal_workcell
3. start everything through docker

        docker compose up

4. check that everythind has started by looking at the dashboard.

    Go to http://localhost:8000/ in a browser. If the rest of the nodes have been started correctly, you will see the nodes in a READY state on the left side of the dashboard.


## Experiment Applications

See `applications/NIDHI/README.md` for instructions on setting up and running the adaptive lab evolution experimental application on the biomedal workcell.
