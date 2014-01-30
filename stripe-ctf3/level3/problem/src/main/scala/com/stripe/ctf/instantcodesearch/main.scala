package com.stripe.ctf.instantcodesearch
import org.rogach.scallop._
import scala.language.reflectiveCalls

object instantcodesearch {
  class Conf(args : Array[String]) extends ScallopConf(args) {
    val server = opt[Boolean]()

    val id = opt[Int](required = false)
    val master = opt[Boolean](required = false)

    mutuallyExclusive(id, master)
    dependsOnAny(server, List(id, master))
  }

  val BasePort = 9090

  def main(args : Array[String]) : Unit = {
    val conf = new Conf(args)
    if (conf.master()) {
      startMasterSearchServer()
    } else if (conf.id.get.isDefined) {
      startSearchServer(conf.id())
    } else {
      conf.printHelp()
      System.exit(1)
    }
  }

  def startSearchServer(id : Integer) : SearchServer = {
    val port = BasePort + id
    println("Starting search server on port " + port)
    new SearchServer(port, id)
  }

  def startMasterSearchServer() : SearchMasterServer = {
    println("Starting master on port " + BasePort)
    new SearchMasterServer(BasePort)
  }
}
