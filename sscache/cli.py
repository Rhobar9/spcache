"""A CLI tool to set the Spotify cache size threshold."""

import typing as t

import click

# TODO: Inspect the behaviour of the Spotify client when the cache size
# is set to 0.

CACHE_KEY = "storage.size"
CTX_SETTINGS = {"help_option_names": ["-h", "--help"]}


@click.command(context_settings=CTX_SETTINGS)
@click.option(
    "--file",
    "-f",
    help="Path to the Spotify prefs file.",
    type=click.Path(exists=True, dir_okay=False, readable=True, writable=True),
    envvar="SPOTIFY_PREFS_FILE",
)
@click.option(
    "--size",
    "-s",
    default=1024,
    help="Cache limit [MB]",
    type=click.IntRange(0, None),
    show_default=True,
    envvar="SPOTIFY_CACHE_SIZE",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Ignore errors in the prefs file.",
    show_default=True,
    envvar="SPOTIFY_IGNORE_ERRORS",
)
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    help="Do not prompt for confirmation after auto-detecting a path.",
    show_default=True,
    envvar="SPOTIFY_YES",
)
@click.version_option(None, "--version", "-V", package_name=__package__)
@click.pass_context
def sscache(ctx: click.Context, file: t.Optional[str], size: int, force: bool, yes: bool) -> None:
    """
    Set the cache size limit on the Spotify prefs file: FILE.

    FILE is the path to the Spotify prefs file.
    FILE may also be specified through the SPOTIFY_PREFS_FILE
    environment variable.
    """
    if file is None:
        from sscache import detect

        file = detect.detect_prefs_file(ctx)
        if file is None:
            ctx.fail(
                "The Spotify prefs file couldn't be auto-detected."
                "\nPlease specify a path to the prefs file using the --file option."
            )

        if not yes:
            click.confirm(
                f"Auto-detected Spotify prefs file: {file}\nIs this correct?",
                abort=True,
            )

    import pathlib

    filepath = pathlib.Path(file)
    if filepath.name != "prefs":
        click.echo(
            f"The given file should be named 'prefs', not '{filepath.name}'. Is the path correct?",
            err=True,
        )

    from sscache import env

    env.set_cache_size(ctx, file, CACHE_KEY, str(size), quote_mode="never", force=force)


if __name__ == "__main__":
    sscache()
