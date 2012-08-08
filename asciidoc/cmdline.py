import os
import sys
import asciidoc

def exec_cmdline(opts, args, messages_out):
    kwargs = dict(
        conf_files=[],
        filters=[],
        attrs={},
        default_attrs={},
        )
    for o,v in opts:
        if o == '--unsafe':
            kwargs['safe'] = False
        if o == '--safe':
            kwargs['safe'] = True
        if o == '--version':
            print('asciidoc %s' % asciidoc.VERSION)
            sys.exit(0)
        if o in ('-b','--backend'):
            kwargs['backend'] = v
        if o in ('-c','--dump-conf'):
            kwargs['dump_conf'] = True
        if o in ('-d','--doctype'):
            kwargs['doctype'] = v
        if o in ('-e','--no-conf'):
            kwargs['no_conf'] = True
        if o in ('-f','--conf-file'):
            kwargs['conf_files'].append(v)
        if o == '--filter':
            kwargs['filters'].append(v)
        if o in ('-n','--section-numbers'):
            kwargs['attrs']['numbered'] = True
        if o == '--theme':
            kwargs['attrs']['theme'] = v
        if o in ('-a','--attribute'):
            e = asciidoc.parse_entry(v, allow_name_only=True)
            if not e:
                usage(g, 'Illegal -a option: %s' % v)
                sys.exit(1)
            k,v = e
            # A @ suffix denotes don't override existing document attributes.
            if v and v[-1] == '@':
                kwargs['default_attrs'][k] = v[:-1]
            else:
                kwargs['attrs'][k] = v
        if o in ('-s','--no-header-footer'):
            kwargs['no_header_footer'] = True
        if o in ('-v','--verbose'):
            kwargs['verbose'] = True

    infile = None
    outfile = None
    inpath = None
    outpath = None
    fst = args[0]
    snd = args[1] if len(args) > 1 else None
    try:
        if fst == '-':
            infile = sys.stdin
        elif isinstance(fst, str) or isinstance(fst, unicode):
            inpath = os.path.abspath(fst)
            infile = open(inpath, 'rb')
        else:
            infile = fst
        if len(args) < 2:
            outfile = sys.stdout
        elif isinstance(snd, str) or isinstance(snd, unicode):
            outpath = os.path.abspath(snd)
            outfile = open(outpath, 'wb+')
        else:
            outfile = snd
        asciidoc.execute(infile, outfile, inpath=inpath, outpath=outpath, **kwargs)
    finally:
        pass
        #if infile != sys.stdin:
        #    infile.close()
        #if outfile != sys.stdout:
        #    outfile.close()
