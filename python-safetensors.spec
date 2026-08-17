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
Release:	1
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
BuildRequires:	rust-packaging

%description
Safetensors is a new simple format for storing tensors safely (as opposed
to pickle) and that is still fast (zero-copy).

%prep -a
tar xf %{SOURCE1}
%cargo_prep -v vendor
# cargo_prep writes a CWD-relative path; maturin/cargo also run from
# bindings/python/
sed -i "s#directory = \"vendor\"#directory = \"$PWD/vendor\"#" .cargo/config.toml

%build -p
export CARGO_HOME=$PWD/.cargo
export CARGO_NET_OFFLINE=true

%build -a
rm -rf bindings/python/.cargo
ln -sfn ../../.cargo bindings/python/.cargo
pushd bindings/python
%cargo_license_summary
%{cargo_license} > ../../LICENSES.dependencies
popd

%files
%doc bindings/python/README.md
%license LICENSE LICENSES.dependencies
%{python_sitearch}/safetensors
%{python_sitearch}/safetensors-%{version}.dist-info
