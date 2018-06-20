import kelte.__metadata__ as package_info
import kelte.api
import kelte.vendored.click as click


@click.command()
@click.option('-d', '--debug', is_flag=True, help='Run in debug mode.')
@click.option('-v', '--verbose', count=True, help='Increase verbosity.')
@click.option('-V', '--version', is_flag=True, help='Show version and exit.')
def run(debug, verbose, version):
    if version:
        print(f'{package_info.__version__}')

    kelte.api.run(debug=debug, verbose=verbose)


if __name__ == '__main__':
    run()
