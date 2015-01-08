############################
Setting up a gh-pages branch
############################

These assume a default sphinx build directory of ``doc/_build``.

Makefile target (don't forget the tabs before the target body lines)::

    git-clean:
        git clean -fxd

    html:
        cd doc && make html

    gh-pages: git-clean html
        git co gh-pages
        git rm -r .
        git checkout HEAD -- .gitignore README.md .nojekyll
        cp -r doc/_build/html/* . # your sphinx build directory
        git stage .
        @echo 'Commit and push when ready or git reset --hard && git checkout master to revert'


Make a new empty ``gh-pages`` branch::

    git checkout --orphan gh-pages
    rm .gitignore
    git clean -fxd
    git reset --hard

Make some files for working with github pages in this branch::

    # Ignore the doc and doc build directory
    echo "doc/" > .gitignore
    echo "Github pages for project" > README.md
    touch .nojekyll
    git add .gitignore .nojekyll README.md
    git commit -m 'Initial commit'

Set the upstream for this branch::

    git push <your-github-remote> gh-pages --set-upstream

Now go back to the master branch::

    git co master
    make gh-pages
