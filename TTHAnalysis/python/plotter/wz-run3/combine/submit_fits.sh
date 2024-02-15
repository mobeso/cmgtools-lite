# Submit all possible fits of the analysis
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color


mode=$1
extra=$2

# --- For year 2022
echo -e "$RED >> 2022 Pre EE $NC"
python run_combine.py --mode $mode -a 2022_     --output fits/2022/inclusive $extra
python run_combine.py --mode $mode -a 2022_eee --output fits/2022/eee $extra
python run_combine.py --mode $mode -a 2022_eem --output fits/2022/eem $extra
python run_combine.py --mode $mode -a 2022_mme --output fits/2022/mme $extra
python run_combine.py --mode $mode -a 2022_mmm --output fits/2022/mmm $extra

# --- For year 2022PostEE
echo -e "$RED >> 2022 Post EE $NC"
python run_combine.py --mode $mode -a 2022EE_     --output fits/2022EE/inclusive $extra
python run_combine.py --mode $mode -a 2022EE_eee --output fits/2022EE/eee $extra
python run_combine.py --mode $mode -a 2022EE_eem --output fits/2022EE/eem $extra
python run_combine.py --mode $mode -a 2022EE_mme --output fits/2022EE/mme $extra
python run_combine.py --mode $mode -a 2022EE_mmm --output fits/2022EE/mmm $extra

# --- For full 2022
echo -e "$RED >> full 2022 $NC"
python run_combine.py --mode $mode        --output fits/all/inclusive $extra
python run_combine.py --mode $mode -a eee --output fits/all/eee $extra
python run_combine.py --mode $mode -a eem --output fits/all/eem $extra
python run_combine.py --mode $mode -a mme --output fits/all/mme $extra
python run_combine.py --mode $mode -a mmm --output fits/all/mmm $extra
