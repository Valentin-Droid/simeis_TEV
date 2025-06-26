cmake_minimum_required(VERSION 3.10)
project(simeis-build)

# Pour exécuter une commande rust
add_custom_target(
    build-release
    COMMAND ${CMAKE_COMMAND} -E env RUSTFLAGS=-C\ code-model=small\ -C\ codegen-units=1 cargo build --release
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Compiling Simeis in release mode"
)

add_custom_target(
    strip-release
    COMMAND strip target/release/simeis-server
    DEPENDS build-release
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Stripping the release binary"
)

add_custom_target(
    check
    COMMAND cargo check
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Running cargo check"
)

add_custom_target(
    test
    COMMAND cargo test
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Running unit tests"
)

add_custom_target(
    clean-all
    COMMAND cargo clean
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Cleaning build artifacts"
)

add_custom_target(
    doc
    COMMAND typst compile doc/manual.typ doc/manual.pdf
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Generating the PDF manual using Typst"
)

