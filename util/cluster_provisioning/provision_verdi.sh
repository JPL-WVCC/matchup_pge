source ./env.sh
curl -O https://cae-artifactory.jpl.nasa.gov/artifactory/${artifactory_repo}/gov/nasa/jpl/iems/sds/pcm/${hysds_release}/hysds-conda_env-${hysds_release}.tar.gz
mkdir -p ~/conda
tar xvfz hysds-conda_env-${hysds_release}.tar.gz -C conda
export PATH=$HOME/conda/bin:$PATH
conda-unpack
rm -rf hysds-conda_env-${hysds_release}.tar.gz
curl -O https://cae-artifactory.jpl.nasa.gov/artifactory/${artifactory_repo}/gov/nasa/jpl/iems/sds/pcm/${hysds_release}/hysds-verdi_venv-${hysds_release}.tar.gz
tar xvfz hysds-verdi_venv-${hysds_release}.tar.gz
rm -rf hysds-verdi_venv-${hysds_release}.tar.gz
