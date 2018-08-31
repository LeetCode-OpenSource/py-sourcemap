#![feature(specialization)]

extern crate pyo3;
extern crate source_map_mappings;

use std::fs::File;
use std::io::{BufReader, Read};

use pyo3::prelude::*;
use source_map_mappings::{Bias, Mappings, parse_mappings};

#[pyclass]
struct SourcemapParser {
  parsed_map: Mappings<()>
}

#[pymethods]
impl SourcemapParser {
  #[new]
  fn __new__(obj: &PyRawObject, path: &str) -> PyResult<()> {
    let file = File::open(path).map_err(PyErr::from)?;
    let mut buffers = vec![];
    let mut reader = BufReader::new(file);
    reader.read_to_end(&mut buffers).map_err(PyErr::from)?;
    let mappings = parse_mappings(&buffers).map_err(|_| PyErr::new::<exc::TypeError, _>(format!("Parse Sourcemap failed: {}", path)))?;
    obj.init(|_| SourcemapParser {
      parsed_map: mappings,
    })
  }

  fn original_location_for(&self, generated_line: u32, generated_column: u32) -> PyResult<(u32, u32)> {
    if let Some(mapping) = self.parsed_map.original_location_for(generated_line, generated_column, Bias::LeastUpperBound) {
      return Ok((mapping.generated_line, mapping.generated_column))
    }
    Err(PyErr::new::<exc::TypeError, _>("No sources found"))
  }
}

#[pymodinit]
fn py_sourcemap(_py: Python, m: &PyModule) -> PyResult<()> {
  m.add_class::<SourcemapParser>()?;
  Ok(())
}
