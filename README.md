# Lattice Competency export Tool

This project will export your competency data ("Align on expectations" within Lattice) to a spreadsheet.

It uses undocumented parts of Lattice's GraphQL API that Lattice uses to build its own pages.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.12 or higher
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management and running the project

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/kbayliss/lattice_export
cd lattice_export
```

Install the project dependencies using Poetry:

```bash
poetry install
```

## Configuration

Before running the script, you need to set up your environment variables by creating a `.env` file. An example file `.env.example` is provided in the repository.

### Setting up the .env file

Copy the `.env.example` to a new file named `.env`.

```bash
cp .env.example .env
```

Fill in the `ACCESS_TOKEN` and `LATTICE_USER_ENTITY_ID` with your own values obtained from Lattice.

#### Obtaining ACCESS_TOKEN

1. Open your web browser and log into your Lattice account.
2. Open the browser's developer tools and go to the Network tab.
3. Filter for `/graphql/` to find a call to the GraphQL API.
4. Look in the request Headers or the Cookies to find the `access_token`. It should look like `access_token=...;`.

#### Finding LATTICE_USER_ENTITY_ID

1. In the developer tools under the Network tab, look for any GraphQL API call payloads.
2. Find the request payload containing `userEntityId: ...` in the variables.

## Running the Script

Once you have your `ACCESS_TOKEN` and `LATTICE_USER_ENTITY_ID`, you can run the script:

```bash
poetry run export
```

## Important notes

- Do not share your `ACCESS_TOKEN` or `LATTICE_USER_ENTITY_ID` as they are sensitive information that can grant access to your personal data on Lattice.

## Contributing

If you'd like to contribute to the project, please fork the repository and create a pull request with your changes.
