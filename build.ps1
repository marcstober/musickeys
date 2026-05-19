pytest

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

py .\musickeycomputer.py
