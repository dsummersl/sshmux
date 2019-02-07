import logging
import subprocess

logger = logging.getLogger('connections')


class Connection(object):
    @classmethod
    def hosts(cls, args):
        raise NotImplementedError()

    @classmethod
    def copy(cls, host, args):
        raise NotImplementedError()

    @classmethod
    def connect(cls, host, args):
        raise NotImplementedError()


class SSHConnection(Connection):
    @classmethod
    def hosts(cls, args):
        if len(args.hosts) == 0:
            print("At least one host must be specified!\n")
            sys.exit(1)
        return args.hosts

    @classmethod
    def copy(cls, host, args):
        return 'scp {} {} {}:/tmp'.format(args.options, args.script, host)

    @classmethod
    def connect(cls, host, args):
        return 'ssh {} {}'.format(args.options, host)


class DockerConnection(Connection):
    @classmethod
    def hosts(cls, args):
        hosts = args.hosts
        if len(hosts) == 0:
            logger.debug('docker ps -q')
            output = subprocess.check_output(['docker ps -q'], shell=True)
            hosts = str(output, 'utf-8').split('\n')
            hosts = [h for h in hosts if len(h) > 0]

        logger.debug("hosts = {0}".format(hosts))

        return hosts

    @classmethod
    def copy(cls, host, args):
        return 'docker cp {} {}:/tmp'.format(args.script, host)

    @classmethod
    def connect(cls, host, args):
        return 'docker exec -it {} {}'.format(host, args.shell)
