#![feature(specialization)]

extern crate pyo3;
extern crate source_map_mappings;
#[macro_use]
extern crate serde_derive;
extern crate serde;
extern crate serde_json;

use std::fs::File;

use pyo3::prelude::*;
use source_map_mappings::{parse_mappings, Bias, Mapping, Mappings};

#[derive(Serialize, Deserialize, Debug)]
#[serde(rename_all = "camelCase")]
struct RawSourceMap {
  version: u8,
  sources: Vec<String>,
  names: Vec<String>,
  mappings: String,
  file: String,
  source_root: Option<String>,
}

#[pyclass]
struct SourcemapParser {
  parsed_map: Mappings<()>,
  sources: Vec<String>,
  names: Vec<String>,
}

#[pymethods]
impl SourcemapParser {
  #[new]
  fn __new__(obj: &PyRawObject, path: &str) -> PyResult<()> {
    let file = File::open(path).map_err(PyErr::from)?;
    let raw_sourcemap: RawSourceMap = serde_json::from_reader(file)
      .map_err(|e| PyErr::new::<exc::TypeError, _>(format!("{:?}", e)))?;
    let mapping_bytes = raw_sourcemap.mappings.as_bytes();
    let mappings = parse_mappings(mapping_bytes)
      .map_err(|_| PyErr::new::<exc::TypeError, _>(format!("Parse Sourcemap failed: {}", path)))?;
    let sources = raw_sourcemap.sources;
    let names = raw_sourcemap.names;
    obj.init(move |_| SourcemapParser {
      parsed_map: mappings,
      sources,
      names,
    })
  }

  fn original_location_for(
    &self,
    generated_line: u32,
    generated_column: u32,
  ) -> PyResult<(u32, u32, Option<String>, Option<String>)> {
    if let Some(Mapping { original, .. }) =
      self
        .parsed_map
        .original_location_for(generated_line - 1, generated_column - 1, Bias::LeastUpperBound)
    {
      match original {
        Some(location) => {
          let name = location.name.and_then(|index| {
            self
              .names
              .get(index as usize)
              .map(|str_slice| str_slice.to_string())
          });
          let source = self
            .sources
            .get(location.source as usize)
            .map(|str_slice| str_slice.to_string());
          return Ok((
            location.original_line + 1,
            location.original_column + 1,
            source,
            name,
          ));
        }
        None => return Err(PyErr::new::<exc::TypeError, _>("No original lines")),
      };
    }
    Err(PyErr::new::<exc::TypeError, _>("No sources found"))
  }
}

#[pymodinit]
fn py_sourcemap(_py: Python, m: &PyModule) -> PyResult<()> {
  m.add_class::<SourcemapParser>()?;
  Ok(())
}
