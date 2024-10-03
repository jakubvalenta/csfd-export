# ČSFD Export

Export your film ratings as a spreadsheet file.

The resulting file is a CSV, which can be
[https://letterboxd.com/about/importing-data/](imported to Letterboxd).

You can find the app at: [csfd-export.ooooo.page](https://csfd-export.ooooo.page).

## Installation

### Mac

```shell
$ brew install poetry
$ make setup
```

### Arch Linux

```shell
# pacman -S python-poetry
$ make setup
```

### Other systems

Install these dependencies manually:

- Python >= 3.11
- poetry

Then run:

```shell
$ make setup
```

## Usage

Start a development server

```shell
$ make run
```

## Contributing

__Feel free to remix this project__ under the terms of the GNU General Public
License version 3 or later. See [COPYING](./COPYING) and [NOTICE](./NOTICE).
