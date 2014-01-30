package com.stripe.ctf.instantcodesearch

import java.io._

class Index(repoPath: String) extends Serializable {
  var files = List[String]()

  def path() = repoPath

  def addFile(file: String, text: String) {
    files = file :: files
  }

  def write(out: File) {
    val stream = new FileOutputStream(out)
    write(stream)
    stream.close
  }

  def write(out: OutputStream) {
    val w = new ObjectOutputStream(out)
    w.writeObject(this)
    w.close
  }
}

