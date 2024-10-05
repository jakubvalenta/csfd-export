# ČSFD Export

Export your film ratings as a spreadsheet file.

The resulting file is a CSV that can be
[https://letterboxd.com/about/importing-data/](imported to Letterboxd).

You can find the app at [csfd-export.ooooo.page](https://csfd-export.ooooo.page).

## Command Line Interface

### Installation

1. Install [Python >= 3.11](https://www.python.org/).

2. Install ČSFD Export as a pip package:

    ``` shell
    $ pip install --user --upgrade .
    ```

    This will make the executable `csfd-export` available globally.

### Usage

#### Fetch ratings for a ČSFD user

Example:

```shell
$ csfd-export https://www.csfd.cz/uzivatel/18708-polaroid/hodnoceni/ my_ratings.csv
```

This will create a file `my_ratings.csv` like this:

```csv
Title,Year,Rating,WatchedDate
The Matrix Resurrections,2021,2,2021-12-29
The Power of Nightmares,2004,5,2021-04-24
Tenkrát v Hollywoodu,2019,0.5,2021-01-30
...
```

### Help

See all command line options:

``` shell
$ csfd-export --help
```

## Web App

### Installation

#### Mac

```shell
$ brew install poetry
$ make setup
```

#### Arch Linux

```shell
# pacman -S python-poetry
$ make setup
```

#### Other systems

Install these dependencies manually:

- Python >= 3.11
- poetry

Then run:

```shell
$ make setup
```

### Usage

Start a development server

```shell
$ make run
```

## Development

### Installation

```shell
$ make setup
```

### Testing and linting

```shell
$ make test
$ make lint
```

### Test Help

```shell
$ make help
```

## Contributing

__Feel free to remix this project__ under the terms of the GNU General Public
License version 3 or later. See [COPYING](./COPYING) and [NOTICE](./NOTICE).
