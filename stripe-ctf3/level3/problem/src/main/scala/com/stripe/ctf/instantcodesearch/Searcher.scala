package com.stripe.ctf.instantcodesearch

import java.io._
import java.nio.file._

import com.twitter.concurrent.Broker

abstract class SearchResult
case class Match(path: String, line: Int) extends SearchResult
case class Done() extends SearchResult

class Searcher(indexPath : String)  {
  val index : Index = readIndex(indexPath)
  val root = FileSystems.getDefault().getPath(index.path)

  def search(needle : String, b : Broker[SearchResult]) = {
    for (path <- index.files) {
      for (m <- tryPath(path, needle)) {
        b !! m
      }
    }

    b !! new Done()
  }

  def tryPath(path: String, needle: String) : Iterable[SearchResult] = {
    try {
      val text : String = slurp(root.resolve(path))
      if (text.contains(needle)) {
        var line = 0
        return text.split("\n").zipWithIndex.
          filter { case (l,n) => l.contains(needle) }.
          map { case (l,n) => new Match(path, n+1) }
      }
    } catch {
      case e: IOException => {
        return Nil
      }
    }

    return Nil
  }

  def readIndex(path: String) : Index = {
    new ObjectInputStream(new FileInputStream(new File(path))).readObject.asInstanceOf[Index]
  }
}
