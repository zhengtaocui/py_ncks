#
# For example, 
# awk -f copy_restart_files.awk /gpfs/hps3/ptmp/Zhengtao.Cui/restartfiles.txt > copyfiles.bash
# chmod +x copyfiles.bash
#
# Then run the copyfiles.bash
#
BEGIN{print "#!/bin/bash"}

NR <=7 {next}
{
   str = $1

   gsub( /Donald\.W.Johnson\/nwtest_output/, "Zhengtao\.Cui\/nwtest_output", str) 
#   str1 = gensub( /^(\/.+)\/[^\/]*\/?$/, "\\1", "g", str)
   str1 = gensub( /\/[^\/]*\/?$/, "", "g", str)
  # gsub( /\/[^\/]*\/?$/, "", str1)
#   print "***", str1
#   print str
   print "if [ ! -d "str1" ]"
   print "then"
   print "   mkdir -p "str1
   print "fi"
   print "scp  -r luna:"$1, str1
}
