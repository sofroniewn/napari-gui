# napari 0.4.4

We're happy to announce the release of napari 0.4.4!
napari is a fast, interactive, multi-dimensional image viewer for Python.
It's designed for browsing, annotating, and analyzing large multi-dimensional
images. It's built on top of Qt (for the GUI), vispy (for performant GPU-based
rendering), and the scientific Python stack (numpy, scipy).


For more information, examples, and documentation, please visit our website:
https://github.com/napari/napari

## Highlights
This release is a quick follow on from our `0.4.3` release and contains some nice improvements to the GUI and 
analysis function hookspecs we experimentally added in that release. We've expanded the API of the
`napari_experimental_provide_dock_widget` to accept new `magic_factory` decorated functions and callables that
return widgets, making it easier for developers who want to use magicgui and not have to write their own qt 
widgets (#2143). At the same time we renamed `napari_experimental_provide_function_widget` to 
`napari_experimental_provide_function` and reduced its API to only accepting a function or list of functions
to make it even easier to build up an analysis function interface (#2158).


## Improvements
- Add example code to hook documentation (#2112)
- move Viewer import into method (#2119)
- Support for EventedList.__setitem__ with array-like items (#2120)
- Add __array__ protocol to transforms.Affine (#2137)
- Relax dock_widget_hookspec to accept callable. (#2143)
- Add name of system to napari sys_info (#2147)
- Points layer enable interactive mode in add mode, don't add point when dragging, addresses #2146 (WIP) (#2148)
- Change plugin window search from naming convention to pypi classifier (#2153)
- Add compress=1 to tifffile imsave call (#2157)
- Add informations on what to do on error in GUI (#2165)


## Bug Fixes
- QtAboutKeyBindings patch (#2132)
- Fix too-late registration of napari types in magicgui (#2139)
- Fix magicgui.FunctionGui deprecation warning (#2164)
- Fix show/ hide of plugin widgets (#2172)


## API Changes
- Drop items to be removed in 0.4.4 (#2144)
- No naming convention, delay dock_widget discovery (#2152)
- Drop magic_kwargs, dock_kwargs from provide_function_widget (#2158)


## Deprecations
- Deprecate layer.status (#1985)


## Build Tools and Support
- Add missed doc string in `import_resources` (#2113)
- Delay import of pkg_resources (#2121)
- Remove duplicate entry in install_requires (#2122)
- Fix typo in deprecation message (#2124)
- DOC: Formatting and Typos. (#2129)
- DOC: Rename Section to conform to numpydocs (Return->Returns) (#2130)
- Provide `make_test_viewer` as a pytest plugin, for external use. (#2131)
- Doc: fix syntax = instead of : (#2141)


## 11 authors added to this release (alphabetical)

- [Alister Burt](https://github.com/napari/napari/commits?author=alisterburt) - @alisterburt
- [Christoph Gohlke](https://github.com/napari/napari/commits?author=cgohlke) - @cgohlke
- [dongyaoli10x](https://github.com/napari/napari/commits?author=dongyaoli10x) - @dongyaoli10x
- [Grzegorz Bokota](https://github.com/napari/napari/commits?author=Czaki) - @Czaki
- [Juan Nunez-Iglesias](https://github.com/napari/napari/commits?author=jni) - @jni
- [Matthias Bussonnier](https://github.com/napari/napari/commits?author=Carreau) - @Carreau
- [nhthayer](https://github.com/napari/napari/commits?author=nhthayer) - @nhthayer
- [Nicholas Sofroniew](https://github.com/napari/napari/commits?author=sofroniewn) - @sofroniewn
- [Robert Haase](https://github.com/napari/napari/commits?author=haesleinhuepf) - @haesleinhuepf
- [Talley Lambert](https://github.com/napari/napari/commits?author=tlambert03) - @tlambert03
- [Volker Hilsenstein](https://github.com/napari/napari/commits?author=VolkerH) - @VolkerH


## 6 reviewers added to this release (alphabetical)

- [Juan Nunez-Iglesias](https://github.com/napari/napari/commits?author=jni) - @jni
- [nhthayer](https://github.com/napari/napari/commits?author=nhthayer) - @nhthayer
- [Nicholas Sofroniew](https://github.com/napari/napari/commits?author=sofroniewn) - @sofroniewn
- [Robert Haase](https://github.com/napari/napari/commits?author=haesleinhuepf) - @haesleinhuepf
- [Talley Lambert](https://github.com/napari/napari/commits?author=tlambert03) - @tlambert03
- [Ziyang Liu](https://github.com/napari/napari/commits?author=ziyangczi) - @ziyangczi