from .producer import producer
from cfgs.samplepaths import samplepaths as paths
class postprocessor_producer(producer):
  name = "postprocesor_producer"
  basecommand = "nanopy_batch.py"
  wz_cfg = "run_WZpostproc_fromNanoAOD_cfg.py"
  module = "wz_seq1" 

  def add_more_options(self, parser):
    self.parser = parser
    parser.add_option("--outname", dest = "outname", type="string", default = paths["processed"],
                      help = "Output (folder) name")
    return
  
  def submit_InCluster(self):
    return self.command 

  def run(self):
    self.doData = "DATA" if self.isData else "MC"
    outname   = "/".join([self.outname])
    
    if self.local_test:
      outname = "prueba"
      self.extra = self.extra + "--option justSummary=True"
      
    year     = self.year
    extra    = self.extra
    doData   = self.doData
 
    self.commandConfs = ["%s"%self.wz_cfg,
                    "-b 'sbatch batchScript.sh'",
                    "--option year='%s'"%year,
                    "--option selectComponents='%s'"%doData,
                    "--output-dir %s/%s/%s"%(outname, self.doData.lower(), year),
                    "%s"%extra]
    return
  
