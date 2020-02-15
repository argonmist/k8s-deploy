while IFS= read -r dest; do
  scp deploy-node.tar.gz deploy-env.sh "$dest:/tmp"
done <deploy-hosts.txt

while IFS= read -r dest; do
  scp other-node.tar.gz other-env.sh "$dest:/tmp"
done <other-hosts.txt

while IFS= read -r dest; do
  scp haproxy-keepalived.tar.gz haproxy-deploy.sh haproxy-env.sh "$dest:/tmp"
done <haproxy-hosts.txt
