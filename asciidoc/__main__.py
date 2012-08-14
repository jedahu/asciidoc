import sys
import asciidoc
import asciidoc.cmdline

asciidoc.is_main = True

def main():
    # Process command line options.
    g = asciidoc.Global()
    g.config.init()
    import getopt
    try:
        #DEPRECATED: --unsafe option.
        opts,args = getopt.getopt(sys.argv[1:],
            'a:b:cd:ef:hno:svw:',
            ['attribute=','backend=','conf-file=','doctype=','dump-conf',
            'help','no-conf','no-header-footer',
            'section-numbers','verbose','version','safe','unsafe',
            'doctest','filter=','theme='])
    except getopt.GetoptError:
        g.message.stderr('illegal command options')
        sys.exit(1)
    opt_names = [opt[0] for opt in opts]
    if '--doctest' in opt_names:
        # Run module doctests.
        import doctest
        options = doctest.NORMALIZE_WHITESPACE + doctest.ELLIPSIS
        failures,tries = doctest.testmod(optionflags=options)
        if failures == 0:
            g.message.stderr('All doctests passed')
            sys.exit(0)
        else:
            sys.exit(1)

    if len(args) == 0 and len(opts) == 0:
        usage(g)
        sys.exit(0)

    for o,v in opts:
        if o in ('--help','-h'):
            if len(args) == 0:
                asciidoc.show_help(g, 'default')
            else:
                asciidoc.show_help(g, args[-1])
            sys.exit(0)

    # Look for plugin management commands.
    count = 0
    cmd = None
    for o,v in opts:
        if o in ('-b','--backend','--filter','--theme'):
            if o == '-b':
                o = '--backend'
            plugin_type = o[2:]
            cmd = v
            if cmd not in asciidoc.Plugin.CMDS:
                continue
            count += 1
    if count > 1:
        die('--backend, --filter and --theme options are mutually exclusive')
    if count == 1:
        # Execute plugin management commands.
        if not cmd:
            die('missing --%s command' % plugin_type)
        if cmd not in asciidoc.Plugin.CMDS:
            die('illegal --%s command: %s' % (plugin_type, cmd))
        plugin = asciidoc.Plugin(g, plugin_type)
        g.config.verbose = bool(set(['-v','--verbose']) & set(opt_names))
        plugin.run(cmd, args)
        sys.exit(0)

    try:
        asciidoc.cmdline.exec_cmdline(opts, args, [])
    except KeyboardInterrupt:
        sys.exit(1)
    sys.exit(0)

if __name__ == '__main__':
  main()
