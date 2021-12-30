echo "latest tag is:"
last_tag=`git rev-list --tags --max-count=1`
last_tag_desc=`git describe --tags "$last_tag"`
echo "$last_tag_desc"
read -p "Enter New Version: " version
sed -i "s/^.*__version__.*$/__version__ = '0.2.65'/g" boom_base/__version__.py
git tag "$version"
git push --tag