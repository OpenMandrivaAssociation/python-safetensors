%undefine _debugsource_packages

# Recreate the vendor archive after a version bump:
#   tar xf safetensors-VERSION.tar.gz
#   cd safetensors-VERSION/bindings/python
#   cargo vendor --locked ../../vendor
#   cd ../..
#   tar cJf python-safetensors-VERSION-vendor.tar.xz vendor
#   abb store python-safetensors-VERSION-vendor.tar.xz

Name:		python-safetensors
Version:	0.8.0
Release:	2
Summary:	Simple, safe way to store and distribute tensors
License:	Apache-2.0
Group:		Development/Python
URL:		https://github.com/huggingface/safetensors
Source0:	https://files.pythonhosted.org/packages/source/s/safetensors/safetensors-%{version}.tar.gz
Source1:	%{name}-%{version}-vendor.tar.xz

BuildSystem:	python
BuildRequires:	cargo
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(maturin)
BuildRequires:	python%{pyver}dist(pip)

%description
Safetensors is a new simple format for storing tensors safely (as opposed
to pickle) and that is still fast (zero-copy).

%prep -a
# The crates are already vendored, so this build does not need rust-packaging.
tar -xf %{SOURCE1}
mkdir -p .cargo
cat > .cargo/config.toml << EOF
[net]
offline = true

[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "$PWD/vendor"
EOF

%build -p
export CARGO_HOME=$PWD/.cargo
export CARGO_NET_OFFLINE=true

%build -a
rm -rf bindings/python/.cargo
ln -sfn ../../.cargo bindings/python/.cargo
pushd bindings/python
cargo tree --workspace --offline --edges no-build,no-dev,no-proc-macro \
	--prefix none --format '{l}: {p}' \
	| sed -e "s: ($(pwd)[^)]*)::g" -e 's: / :/:g' -e 's:/: OR :g' \
	| sort -u > ../../LICENSES.dependencies
popd

%files
%doc bindings/python/README.md
%license LICENSE LICENSES.dependencies
%{python_sitearch}/safetensors
%{python_sitearch}/safetensors-%{version}.dist-info
